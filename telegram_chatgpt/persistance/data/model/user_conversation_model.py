from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UserConversationModel(Base):
    __tablename__ = 'user_conversation'
    user_id = Column(Integer, primary_key=True)
    conversation = Column(JSON)

    def __str__(self) -> str:
        return f"UserConversation(id={self.user_id}, conversation={self.conversation})"

    def __repr__(self) -> str:
        return f"UserConversation(id={self.user_id}, conversation={self.conversation})"
