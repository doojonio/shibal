import asyncio
import io

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.services.drive import DriveService
from app.tasks import change_volume as queue_change_volume

from .common import back, p, save_input_cb, start
from .values import Commands, Fields, States


async def add_volume_init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Введите количество децибел, на которое нужно увеличить громкость"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if not update.callback_query:
        raise ValueError("Missing update.callback query")

    if context.user_data is None:
        raise ValueError("Missing context.user_data")

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg)
    await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    return States.TYPING_VOLUME


async def reduce_volume_init(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    msg = "Введите количество децибел, на которое нужно уменьшить громкость"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if not update.callback_query:
        raise ValueError("Missing update.callback query")

    if context.user_data is None:
        raise ValueError("Missing context.user_data")

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg)
    await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    return States.TYPING_VOLUME


def get_process_cb(add: bool):
    async def process_change_volume(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> States:
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

        volume = context.user_data[Fields.VOLUME]

        if not add:
            volume *= -1

        async_result = queue_change_volume.delay(id_in_drive, volume)

        while not async_result.ready():
            await asyncio.sleep(1)

        if async_result.failed():
            await update.message.reply_text(
                "Извините, произошла ошибка, попробуйте снова"
            )
            return await start(update, context)

        name_id = async_result.get()
        input_file = InputFile(await drive.get(name_id), name_id)

        await update.message.reply_document(input_file)

        return await start(update, context)

    return process_change_volume


def get_add_volume_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(add_volume_init, pattern=p(Commands.VOLUME_UP)),
        ],
        states={
            States.TYPING_VOLUME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.VOLUME,
                        invalid_msg="Пожалуйста, введите число",
                        current_state=States.TYPING_VOLUME,
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(
                    filters.ATTACHMENT | filters.AUDIO, get_process_cb(add=True)
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )


def get_reduce_volume_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(reduce_volume_init, pattern=p(Commands.VOLUME_DOWN)),
        ],
        states={
            States.TYPING_VOLUME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.VOLUME,
                        invalid_msg="Пожалуйста, введите число",
                        current_state=States.TYPING_VOLUME,
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(
                    filters.ATTACHMENT | filters.AUDIO, get_process_cb(add=False)
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )
