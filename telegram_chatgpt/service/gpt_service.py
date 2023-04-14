from typing import Dict, List
import logging

from persistance.repository.user_conversation_repository import UserConversationRepository
from persistance.data.dto.user_conversation_dto import UserConversationDto

from helper.gpt_adapter import GPTAdapter

from util.base64_utils import Base64Utils

from exception.chat_exception import ChatException


class GPTService():
    def __init__(self) -> None:
        self.__gpt = GPTAdapter()
        self.__logger = logging.getLogger(self.__class__.__name__)

        self.__user_conversation_repository = UserConversationRepository()

    def __get_message_history(self, user_id: int):
        message_history = []
        userConversation = self.__user_conversation_repository.find_by_id(user_id)
        if(userConversation):
            message_history = userConversation.conversation
        else:
            self.__user_conversation_repository.add(UserConversationDto(user_id=user_id, conversation=[]))
        return message_history

    async def __get_model_answer(self, user_id: int, message_history: List[Dict]):
        model_output = await self.__gpt.inference(message_history=message_history)

        message_history.append({"role": "assistant", "content": model_output})
        self.__user_conversation_repository.update(user_id, UserConversationDto(conversation=message_history))

        return model_output

    async def complete(self, user_id: int, user_message: str) -> str:
        message_history = self.__get_message_history(user_id)
        message_history.append({"role": "user", "content": user_message})

        model_answer = await self.__get_model_answer(
            user_id=user_id,
            message_history=message_history
        )

        self.__logger.info(f"User id:{user_id} | User input base64:{Base64Utils.to_base64(user_message)} | Model answer base64:{Base64Utils.to_base64(model_answer)}")

        return model_answer

    async def regenerate_last_response(self, user_id: int) -> str:
        message_history = self.__get_message_history(user_id)

        if(len(message_history) == 0):
            raise ChatException("Chat history is clean")

        model_answer = await self.__get_model_answer(
            user_id=user_id,
            message_history=message_history
        )

        last_user_input = message_history[-1]["content"]

        self.__logger.info(f"User id:{user_id} | User input base64:{Base64Utils.to_base64(last_user_input)} | Model answer base64:{Base64Utils.to_base64(model_answer)}")

        return model_answer

    def clear_chat_history(self, user_id: int) -> str:
        self.__user_conversation_repository.update(user_id, UserConversationDto(conversation=[]))
