from dataclasses import dataclass

@dataclass
class UserSession:
    access_token : str
    refresh_session : str

