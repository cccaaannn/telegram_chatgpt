from dataclasses import dataclass, field
from typing import Dict


@dataclass
class UserConversationDto:
    user_id: int | None = None
    conversation: Dict[str, str] = field(default_factory=Dict)
