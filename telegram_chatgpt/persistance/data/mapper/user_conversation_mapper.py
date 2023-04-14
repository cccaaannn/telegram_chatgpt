from typing import List

from persistance.data.model.user_conversation_model import UserConversationModel
from persistance.data.dto.user_conversation_dto import UserConversationDto


class UserConversationMapper:

    @staticmethod
    def to_dto(user_conversation_model: UserConversationModel) -> UserConversationDto:
        return UserConversationDto(
            user_id=user_conversation_model.user_id,
            conversation=user_conversation_model.conversation["messages"]
        )

    @staticmethod
    def to_dto_list(user_conversation_model: List[UserConversationModel]) -> List[UserConversationDto]:
        return [
            UserConversationDto(
                user_id=user_conversation.user_id,
                conversation=user_conversation.conversation["messages"]
            )
            for user_conversation in user_conversation_model
        ]

    @staticmethod
    def to_entity(user_conversation_dto: UserConversationDto) -> UserConversationModel:
        return UserConversationModel(
            user_id=user_conversation_dto.user_id,
            conversation={"messages": user_conversation_dto.conversation}
        )
