#!/usr/bin/env python

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
)

from app.config import settings
from app.tg.common import start
from app.tg.convo_cut import get_cut_conv_handler
from app.tg.convo_trim import get_trim_conv_handler
from app.tg.values import States

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.CMD_CHOOSE: [
                get_cut_conv_handler(),
                get_trim_conv_handler(),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
