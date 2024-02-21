from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id: str
    isGuest: bool
    isPremium: bool
    userToken: str
    userLevel: int

class UserUpdate(BaseModel):
    isGuest: Optional[bool] = None
    isPremium: Optional[bool] = None
    userToken: Optional[str] = None
    userLevel: Optional[int] = None