from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    company_name: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    role: Literal["employee", "admin", "hr"] = "employee"
    department: str | None = None
    designation: str | None = None
    date_of_joining: date = Field(default_factory=date.today)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    first_login: bool
    employee_id: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordChange(BaseModel):
    current_password: str | None = None
    new_password: str
    confirm_password: str
