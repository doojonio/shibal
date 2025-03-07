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
from app.tasks.fades import add_fades as queue_add_fades

from .common import back, p, save_input_cb, start
from .values import Commands, Fields, States


async def fades_init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Пожалуйста, введите секунду до которой будет продолжаться фейд-ин"
    buttons = [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]

    if not update.callback_query:
        raise ValueError("Missing update.callback query")

    if context.user_data is None:
        raise ValueError("Missing context.user_data")

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg)
    await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    return States.TYPING_FADE_IN


async def process_fades(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
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

    fade_in_sec = context.user_data[Fields.FADE_IN]
    fade_out_sec = context.user_data[Fields.FADE_OUT]

    async_result = queue_add_fades.delay(
        id_in_drive, int(fade_in_sec * 1000), int(fade_out_sec * 1000)
    )

    while not async_result.ready():
        await asyncio.sleep(1)

    if async_result.failed():
        if "Invalid length" in async_result.traceback:
            await update.message.reply_text(
                "Извините, но введенные значения не соответствуют длине файла"
            )
        else:
            await update.message.reply_text(
                "Извините, произошла ошибка, попробуйте снова"
            )
        return await start(update, context)

    name_id = async_result.get()
    input_file = InputFile(await drive.get(name_id), name_id)

    await update.message.reply_document(input_file)

    return await start(update, context)


def get_fades_conv_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(fades_init, pattern=p(Commands.FADES)),
        ],
        states={
            States.TYPING_FADE_IN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.FADE_IN,
                        current_state=States.TYPING_FADE_IN,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, введите секунду, с который начнется фейд-аут",
                        next_state=States.TYPING_FADE_OUT,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.TYPING_FADE_OUT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.FADE_OUT,
                        invalid_msg="Пожалуйста, введите число",
                        current_state=States.TYPING_FADE_OUT,
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(filters.ATTACHMENT | filters.AUDIO, process_fades),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )
