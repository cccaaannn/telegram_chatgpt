import logging
import argparse
import sys
import os

from dotenv import load_dotenv

from application.telegram_application import TelegramApplication

from helper.db_helper import DBHelper

from util.env_utils import ConfigEnvNames
from util.logger_utils import LoggerUtils


class Cli:
    def __init__(self) -> None:
        env_file = ".env" if os.path.isfile(".env") else ".env.default"
        load_dotenv(env_file)
        LoggerUtils.init_logger()
        DBHelper().init_db()

        self.__logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        parser = argparse.ArgumentParser(description="Telegram gpt", epilog=f"Uses environment variable <{ConfigEnvNames.TELEGRAM_BOT_API_ENVIRONMENT_NAME.value}> <{ConfigEnvNames.OPENAI_API_ENVIRONMENT_NAME.value}> for the api keys if no arguments passed.")
        parser.add_argument("-t", "--telegram", dest="telegram_api_key", metavar="<telegram>", type=str, help="Telegram bot api key")
        parser.add_argument("-o", "--openai", dest="openai_api_key", metavar="<openai>", type=str, help="Openai api key")

        args = parser.parse_args()

        if(args.telegram_api_key):
            os.environ[ConfigEnvNames.TELEGRAM_BOT_API_ENVIRONMENT_NAME.value] = args.telegram_api_key

        if(args.openai_api_key):
            os.environ[ConfigEnvNames.OPENAI_API_ENVIRONMENT_NAME.value] = args.openai_api_key

        if(not os.environ.get(ConfigEnvNames.TELEGRAM_BOT_API_ENVIRONMENT_NAME.value, None)):
            self.__logger.error(f"A telegram bot key must presents at {ConfigEnvNames.TELEGRAM_BOT_API_ENVIRONMENT_NAME.value} environment variable or must be provided via cli argument '-t'")
            sys.exit(1)

        if(not os.environ.get(ConfigEnvNames.OPENAI_API_ENVIRONMENT_NAME.value, None)):
            self.__logger.error(f"A openai api key must presents at {ConfigEnvNames.OPENAI_API_ENVIRONMENT_NAME.value} environment variable or must be provided via cli argument '-o'")
            sys.exit(1)

        t = TelegramApplication()
        t.create_bot()
