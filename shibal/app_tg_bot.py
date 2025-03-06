#!/usr/bin/env python

"""Basic example for a bot that can receive payments from users."""

import asyncio
import logging
from enum import IntEnum, StrEnum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.config import settings
from app.services.drive import DriveService
from app_queue import trim_start as queue_trim_start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class Commands(StrEnum):
    TRIM_START = "TRIM_START"
    CUT = "CUT"
    TRIM_END = "TRIM_END"
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    BACK = "BACK"


class States(StrEnum):
    CMD_CHOOSE = "CMD_CHOOSE"
    TYPING = "TYPING"
    UPLOAD = "UPLOAD"
    STOP = "STOP"


class Flags(IntEnum):
    START_OVER = 10


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = (
        "Я могу просто и быстро редактировать аудио-файлы: "
        "обрезать или изменять громкость. Что вы хотите?"
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Обрезать начало", callback_data=Commands.TRIM_START
            ),
            InlineKeyboardButton(text="Вырезать", callback_data=Commands.CUT),
            InlineKeyboardButton(
                text="Обрезать конец", callback_data=Commands.TRIM_END
            ),
        ],
        [
            InlineKeyboardButton(
                text="Увеличить громкость",
                callback_data=Commands.VOLUME_UP,
            ),
            InlineKeyboardButton(
                text="Понизить громкость",
                callback_data=Commands.VOLUME_DOWN,
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    if (
        (udata := context.user_data)
        and udata.get(Flags.START_OVER)
        and update.callback_query
    ):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg, reply_markup=keyboard)
    elif update.message:
        await update.message.reply_text(msg, reply_markup=keyboard)

    if context.user_data is not None:
        context.user_data[Flags.START_OVER] = False

    return States.CMD_CHOOSE


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if (udata := context.user_data) is not None:
        udata[Flags.START_OVER] = True

    return await start(update, context)


async def trim_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Введите количество секунд, которые нужно отрезать от начала"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg)
        await update.callback_query.edit_message_reply_markup(
            InlineKeyboardMarkup(buttons)
        )

    return States.TYPING


async def cut(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Сколько секунд вы хотите отрезать от начала?"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg)

    return States.TYPING


async def trim_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Сколько секунд вы хотите отрезать от начала?"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg)

    return States.TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if not update.message:
        return States.TYPING

    if context.user_data is not None:
        context.user_data["typed"] = update.message.text

        await update.message.reply_text("Пожалуйста, загрузите аудио файл")

        return States.UPLOAD

    await update.message.reply_text("Введите число, а не эту чушь")

    return States.TYPING


async def process_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if not update.message:
        return States.STOP

    if audio := update.message.audio:
        print("audio ", audio.file_name)
        await update.message.reply_audio(audio)
    elif document := update.message.document:
        file = await document.get_file()
        await file.download_to_drive("./tmp/downloaded.wav")
        drive = DriveService()
        drive.put_from("source_in_drive.wav", "./tmp/downloaded.wav")

        if context.user_data and (sec := context.user_data.get("typed")):
            async_result = queue_trim_start.delay(
                "source_in_drive.wav", float(sec) * 1000
            )

            while not async_result.ready():
                await asyncio.sleep(1)

            if async_result.failed():
                raise ValueError("Fuck UP!")

            result = drive.get(async_result.get())
            await update.message.reply_document(result)

    return await start(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text("До свидания")

    print("STOP")
    return ConversationHandler.END


def _p(val: str) -> str:
    return "^" + val + "$"


def main() -> None:
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    trim_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(trim_start, pattern=_p(Commands.TRIM_START)),
            CallbackQueryHandler(cut, pattern=_p(Commands.CUT)),
            CallbackQueryHandler(trim_end, pattern=_p(Commands.TRIM_END)),
        ],
        states={
            States.TYPING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_input),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(filters.ATTACHMENT | filters.AUDIO, process_audio)
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[CommandHandler("stop", stop)],
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.CMD_CHOOSE: [
                trim_handler,
            ],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
