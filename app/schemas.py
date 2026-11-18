from datetime import date as date_type
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- Auth ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Transactions ----------
class TransactionCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category: str
    date: date_type


class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    date: Optional[date_type] = None


class TransactionOut(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date_type
    owner_id: int

    model_config = ConfigDict(from_attributes=True)