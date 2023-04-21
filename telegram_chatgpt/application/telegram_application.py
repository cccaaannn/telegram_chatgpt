import textwrap
import logging
import sys
import os

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update

from service.gpt_service import GPTService

from util.env_utils import ConfigEnvNames

from exception.gpt_prediction_exception import GPTPredictionException
from exception.chat_exception import ChatException


class TelegramApplication():
    def __init__(self) -> None:
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__gpt_service = GPTService()

    def create_bot(self):
        async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Catches all exceptions if not catch before"""

            exc_type, exc_obj, exc_tb = sys.exc_info()

            if exc_type == GPTPredictionException:
                user_id = update.message.from_user.id
                await context.bot.send_message(chat_id=user_id, text=str(exc_obj))
                return

            if exc_type == ChatException:
                user_id = update.message.from_user.id
                await context.bot.send_message(chat_id=user_id, text=str(exc_obj))
                return

            self.__logger.error("Exception while handling an update", exc_info=context.error)
            try:
                user_id = update.message.from_user.id
                await context.bot.send_message(chat_id=user_id, text="Something went wrong")
            except:
                self.__logger.error("Could not inform user for exception", exc_info=context.error)

        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.__logger.info(f"User: {update.message.from_user}")

            help_text = textwrap.dedent(f"""\
                [Commands]

                [Chat]
                /reset (Resets conversation history)
                /regen or /regenerate (Regenerates last response)

                [Utilities]
                /about
                /help
                """)
            await update.message.reply_text(help_text)

        async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.__logger.info(f"User: {update.message.from_user}")

            help_text = textwrap.dedent("""\
                [About]

                Telegram ChatGPT is an open source project visit projects GitHub page
                https://github.com/cccaaannn/telegram_chatgpt

                Author Can Kurt""")
            await update.message.reply_text(help_text)

        async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.__logger.info(f"User: {update.message.from_user}")

            user_id = update.message.from_user.id
            self.__gpt_service.clear_chat_history(user_id)
            await update.message.reply_text("Conversation reset")

        async def regenerate_answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.__logger.info(f"User: {update.message.from_user}")

            user_id = update.message.from_user.id
            model_answer = await self.__gpt_service.regenerate_last_response(user_id)
            await update.message.reply_text(model_answer)

        async def complete_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            self.__logger.info(f"User: {update.message.from_user}")

            user_id = update.message.from_user.id
            user_input = update.message.text
            model_answer = await self.__gpt_service.complete(user_id, user_input)
            await update.message.reply_text(model_answer)

        self.__logger.info("Starting bot")
        application = Application.builder().token(
            os.environ[ConfigEnvNames.TELEGRAM_BOT_API_ENVIRONMENT_NAME.value]).build()

        application.add_handler(CommandHandler("reset", reset_command))
        application.add_handler(CommandHandler("regen", regenerate_answer_command))
        application.add_handler(CommandHandler("regenerate", regenerate_answer_command))

        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))

        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, complete_chat))

        application.add_error_handler(global_error_handler)

        application.run_polling()
