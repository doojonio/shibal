#!/usr/bin/env python

"""Basic example for a bot that can receive payments from users."""

import asyncio
import io
import logging
from enum import IntEnum, StrEnum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update
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
from app_queue import cut as queue_cut
from app_queue import trim as queue_trim

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class Commands(StrEnum):
    TRIM = "TRIM"
    CUT = "CUT"
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    BACK = "BACK"


class States(StrEnum):
    CMD_CHOOSE = "CMD_CHOOSE"
    TYPING_TRIM_START = "TYPING_TRIM_START"
    TYPING_TRIM_END = "TYPING_TRIM_END"
    TYPING_CUT_START = "TYPING_CUT_START"
    TYPING_CUT_END = "TYPING_CUT_END"
    UPLOAD = "UPLOAD"
    STOP = "STOP"


class Fields(IntEnum):
    CURRENT_FIELD = 9
    START_OVER = 10
    TRIM_START = 11
    TRIM_END = 12
    CUT_START = 13
    CUT_END = 14
    VOLUME_UP = 15
    VOLUME_DOWN = 16


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = (
        "Я могу просто и быстро редактировать аудио-файлы: "
        "обрезать или изменить громкость. Что вы хотите?"
    )

    buttons = [
        [
            InlineKeyboardButton(text="Обрезать", callback_data=Commands.TRIM),
            InlineKeyboardButton(text="Вырезать", callback_data=Commands.CUT),
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
        and udata.get(Fields.START_OVER)
        and update.callback_query
    ):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg, reply_markup=keyboard)
    elif update.message:
        await update.message.reply_text(msg, reply_markup=keyboard)

    if context.user_data is not None:
        context.user_data[Fields.START_OVER] = False

    return States.CMD_CHOOSE


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if (udata := context.user_data) is not None:
        udata[Fields.START_OVER] = True

    return await start(update, context)


async def trim_init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Введите количество секунд, которые нужно отрезать от начала"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if not update.callback_query:
        raise ValueError("Missing update.callback query")

    if context.user_data is None:
        raise ValueError("Missing context.user_data")

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg)
    await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    return States.TYPING_TRIM_START


async def cut_init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Введите секунду, с которой начинается отрезок, который нужно вырезать"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if not update.callback_query:
        raise ValueError("Missing update.callback query")

    if context.user_data is None:
        raise ValueError("Missing context.user_data")

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg)
    await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    return States.TYPING_CUT_START


def _save_input_cb(
    field: Fields, invalid_msg: str, next_msg: str, next_state: States, check_cb=float
):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]
    )

    async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
        if not update.message:
            return States.TYPING_TRIM_START

        if context.user_data is None:
            raise ValueError("Missing context.user_data")

        value = update.message.text

        try:
            checked = check_cb(value)
        except ValueError:
            await update.message.reply_text(invalid_msg, reply_markup=keyboard)
            return States.TYPING_TRIM_START

        context.user_data[field] = checked

        await update.message.reply_text(next_msg, reply_markup=keyboard)
        return next_state

    return save_input


async def process_trim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if not update.message:
        raise ValueError("Missing update.message")
    if not context.user_data:
        raise ValueError("Missing context.user_data")

    doc = update.message.audio or update.message.document
    if not doc:
        await update.message.reply_text("Загрузите, пожалуйста, аудиофайл")
        return States.UPLOAD

    file_name = doc.file_name
    file = await doc.get_file()

    buf = io.BytesIO()
    await file.download_to_memory(buf)
    buf.seek(0)

    drive = DriveService()
    id_in_drive = await drive.put(file_name or "unnamed", buf.read())

    trim_start_sec = context.user_data[Fields.TRIM_START]
    trim_end_sec = context.user_data[Fields.TRIM_END]

    async_result = queue_trim.delay(
        id_in_drive, trim_start_sec * 1000, trim_end_sec * 1000
    )

    while not async_result.ready():
        await asyncio.sleep(1)

    if async_result.failed():
        raise ValueError("Worker did not succeed")

    name_id = async_result.get()
    input_file = InputFile(await drive.get(name_id), name_id)

    await update.message.reply_document(input_file)

    return await start(update, context)


async def process_cut(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    if not update.message:
        raise ValueError("Missing update.message")
    if not context.user_data:
        raise ValueError("Missing context.user_data")

    doc = update.message.audio or update.message.document
    if not doc:
        await update.message.reply_text("Загрузите, пожалуйста, аудиофайл")
        return States.UPLOAD

    file_name = doc.file_name
    file = await doc.get_file()

    buf = io.BytesIO()
    await file.download_to_memory(buf)
    buf.seek(0)

    drive = DriveService()
    id_in_drive = await drive.put(file_name or "unnamed", buf.read())

    start_sec = context.user_data[Fields.CUT_START]
    end_sec = context.user_data[Fields.CUT_END]

    if start_sec >= end_sec:
        raise ValueError("TODO")

    async_result = queue_cut.delay(id_in_drive, start_sec * 1000, end_sec * 1000)

    while not async_result.ready():
        await asyncio.sleep(1)

    if async_result.failed():
        raise ValueError("Worker did not succeed")

    name_id = async_result.get()
    input_file = InputFile(await drive.get(name_id), name_id)

    await update.message.reply_document(input_file)

    return await start(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text("До свидания")

    return ConversationHandler.END


def _p(val: str) -> str:
    return "^" + val + "$"


def main() -> None:
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    trim_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(trim_init, pattern=_p(Commands.TRIM)),
        ],
        states={
            States.TYPING_TRIM_START: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    _save_input_cb(
                        field=Fields.TRIM_START,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, введите число секунд, которое нужно обрезать с конца",
                        next_state=States.TYPING_TRIM_END,
                    ),
                ),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
            States.TYPING_TRIM_END: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    _save_input_cb(
                        field=Fields.TRIM_END,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(filters.ATTACHMENT | filters.AUDIO, process_trim),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )

    cut_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(cut_init, pattern=_p(Commands.CUT)),
        ],
        states={
            States.TYPING_CUT_START: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    _save_input_cb(
                        field=Fields.CUT_START,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, введите секунду, которой заканчивается отрезок, который надо вырезать",
                        next_state=States.TYPING_CUT_END,
                    ),
                ),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
            States.TYPING_CUT_END: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    _save_input_cb(
                        field=Fields.CUT_END,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(filters.ATTACHMENT | filters.AUDIO, process_cut),
                CallbackQueryHandler(back, pattern=_p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.CMD_CHOOSE: [
                trim_conv_handler,
                cut_conv_handler,
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
