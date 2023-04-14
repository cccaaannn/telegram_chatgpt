import logging
import os

from util.env_utils import ConfigEnvNames
from util.file_utils import FileUtils


class LoggerUtils:

    @staticmethod
    def init_logger() -> None:
        """Sets up logger"""

        logging.getLogger().setLevel(int(os.getenv(ConfigEnvNames.LOG_LEVEL.value)))

        log_file_path = FileUtils.create_abs_aware_parent_dir(
            os.getenv(ConfigEnvNames.LOG_FILE.value))

        logging.basicConfig(
            format="[%(name)s] [%(levelname)s] (%(threadName)s-%(thread)d) (%(asctime)s.%(msecs)03d) (%(funcName)s) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
