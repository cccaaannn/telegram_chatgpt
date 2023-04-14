from typing import List
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer

from persistance.data.mapper.user_conversation_mapper import UserConversationMapper
from persistance.data.model.user_conversation_model import UserConversationModel
from persistance.data.dto.user_conversation_dto import UserConversationDto

from helper.db_helper import DBHelper

from exception.record_not_found_exception import RecordNotFoundException


class UserConversationRepository():
    def __init__(self) -> None:
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__db_utils = DBHelper()

    def add(self, user_conversation_dto: UserConversationDto) -> None:
        with sessionmaker(self.__db_utils.get_db_engine()).begin() as session:
            session.add(UserConversationMapper.to_entity(
                user_conversation_dto))
            self.__logger.debug(f"Record saved to db {user_conversation_dto}")

    def update(self, user_id: Integer, user_conversation_dto: UserConversationDto) -> None:
        with sessionmaker(self.__db_utils.get_db_engine()).begin() as session:
            oldUserConversation = session.query(
                UserConversationModel).filter_by(user_id=user_id).first()

            if(not oldUserConversation):
                raise RecordNotFoundException(
                    f"Record not found with user id {user_id}")

            oldUserConversation.conversation = UserConversationMapper.to_entity(
                user_conversation_dto).conversation

            self.__logger.debug(
                f"Record with id {user_id} updated {user_conversation_dto}")

    def delete_by_id(self, user_id: Integer) -> None:
        with sessionmaker(self.__db_utils.get_db_engine()).begin() as session:
            user_conversation = session.query(
                UserConversationModel).filter_by(user_id=user_id).first()

            if(not user_conversation):
                raise RecordNotFoundException()

            session.delete(user_conversation)

            self.__logger.debug(f"Record removed with id {user_id}")

    def find_by_id(self, user_id: Integer) -> (UserConversationDto | None):
        with sessionmaker(self.__db_utils.get_db_engine()).begin() as session:
            user_conversation = session.query(
                UserConversationModel).filter_by(user_id=user_id).first()
            if(user_conversation):
                return UserConversationMapper.to_dto(user_conversation)
            return None

    def find_all(self) -> List[UserConversationDto]:
        with sessionmaker(self.__db_utils.get_db_engine()).begin() as session:
            user_conversations = session.query(UserConversationModel).all()
            return UserConversationMapper.to_dto_list(user_conversations)
