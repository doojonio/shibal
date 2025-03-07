from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
)

from .values import Commands, Fields, States


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    msg = "Я могу просто и быстро редактировать аудио-файлы. Что вы хотите?"

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
        [
            InlineKeyboardButton(text="Добавить фейды", callback_data=Commands.FADES),
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


def save_input_cb(
    field: Fields,
    invalid_msg: str,
    current_state: States,
    next_msg: str,
    next_state: States,
    check_cb=float,
):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Назад", callback_data=Commands.BACK)]]
    )

    async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
        if not update.message:
            return current_state

        if context.user_data is None:
            raise ValueError("Missing context.user_data")

        value = update.message.text

        try:
            checked = check_cb(value)
        except ValueError:
            await update.message.reply_text(invalid_msg, reply_markup=keyboard)
            return current_state

        context.user_data[field] = checked

        await update.message.reply_text(next_msg, reply_markup=keyboard)
        return next_state

    return save_input


def p(*vals: str) -> str:
    return "^" + "|".join(vals) + "$"
