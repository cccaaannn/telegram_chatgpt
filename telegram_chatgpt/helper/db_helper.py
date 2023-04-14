import logging
import os

from sqlalchemy import create_engine

from persistance.data.model.user_conversation_model import Base as UserConversationBase

from util.env_utils import ConfigEnvNames
from util.file_utils import FileUtils


class DBHelper():
    def __init__(self) -> None:
        self.__logger = logging.getLogger(self.__class__.__name__)

        db_file_path = FileUtils.create_abs_aware_parent_dir(os.getenv(ConfigEnvNames.DB_PATH.value))
        self.__engine = create_engine(f'sqlite:///{db_file_path}')

    def get_db_engine(self):
        return self.__engine

    def init_db(self):
        self.__logger.info("Initializing database")
        UserConversationBase.metadata.create_all(self.get_db_engine())
