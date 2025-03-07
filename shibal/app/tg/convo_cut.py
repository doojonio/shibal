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
from app.tasks import cut as queue_cut

from .common import back, p, save_input_cb, start
from .values import Commands, Fields, States


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
        await update.message.reply_text(
            "Секунда начала отрезка не может быть больше секунды его конца!"
        )
        return await start(update, context)

    async_result = queue_cut.delay(id_in_drive, start_sec * 1000, end_sec * 1000)

    while not async_result.ready():
        await asyncio.sleep(1)

    if async_result.failed():
        if "Invalid length" in async_result.traceback:
            await update.message.reply_text(
                "Введенные значения не соответствуют длине файла"
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


def get_cut_conv_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(cut_init, pattern=p(Commands.CUT)),
        ],
        states={
            States.TYPING_CUT_START: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.CUT_START,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, введите секунду, которой заканчивается отрезок, который надо вырезать",
                        next_state=States.TYPING_CUT_END,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.TYPING_CUT_END: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_input_cb(
                        field=Fields.CUT_END,
                        invalid_msg="Пожалуйста, введите число",
                        next_msg="Пожалуйста, загрузите аудио-файл",
                        next_state=States.UPLOAD,
                    ),
                ),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
            States.UPLOAD: [
                MessageHandler(filters.ATTACHMENT | filters.AUDIO, process_cut),
                CallbackQueryHandler(back, pattern=p(Commands.BACK)),
            ],
        },
        map_to_parent={States.CMD_CHOOSE: States.CMD_CHOOSE},
        fallbacks=[
            CommandHandler("start", start),
        ],
    )
