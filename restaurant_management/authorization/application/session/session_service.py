from abc import ABC, abstractmethod
from typing import Dict, Any

class SessionService(ABC):
    @abstractmethod
    def delete_session(self, refresh_token: str) -> None:
        pass

    @abstractmethod
    def refresh_session(self, refresh_token: str) -> Dict[str, str]:
        pass

    @abstractmethod
    def create_session(self, user: Any) -> Dict[str, str]:
        pass