from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.auth import UserRegister, UserLogin, PasswordChange, RefreshTokenRequest
from app.services import auth_service
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.utils.response import success_response
from app.exceptions import ForbiddenException, UnauthorizedException

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register")
async def register_employee(
    data: UserRegister, 
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(None, alias="Authorization"),
):
    result = await db.execute(select(User).limit(1))
    first_user = result.scalar_one_or_none()
    
    if first_user:
        if not authorization or not authorization.startswith("Bearer "):
            raise UnauthorizedException("Authorization required. Only admins can register new users.")

        token = authorization.split(" ", 1)[1]
        payload = decode_token(token)
        employee_id = payload.get("sub")
        if not employee_id:
            raise UnauthorizedException("Invalid token payload")

        result = await db.execute(select(User).where(User.employee_id == employee_id))
        admin = result.scalar_one_or_none()
        if not admin or not admin.is_active:
            raise UnauthorizedException("User not found or inactive")

        if admin.role not in ["admin", "hr"]:
            raise ForbiddenException("Admin/HR access required")
    else:
        data.role = "admin"

    user, temp_password = await auth_service.register_employee(db, data)
    return success_response(
        data={"user": {"employee_id": user.employee_id, "email": user.email}, "temp_password": temp_password},
        message="Employee registered successfully"
    )

@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate(db, data.email, data.password)
    tokens = {
        "access_token": create_access_token({"sub": user.employee_id}),
        "refresh_token": create_refresh_token({"sub": user.employee_id}),
        "token_type": "bearer",
        "role": user.role,
        "first_login": user.first_login,
        "employee_id": user.employee_id
    }
    return success_response(data=tokens, message="Login successful")

@router.post("/refresh")
async def refresh_token(req: RefreshTokenRequest):
    payload = decode_token(req.refresh_token)
    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid refresh token")
    employee_id = payload.get("sub")
    access_token = create_access_token({"sub": employee_id})
    return success_response(data={"access_token": access_token}, message="Token refreshed")

@router.post("/change-password")
async def change_password(data: PasswordChange, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await auth_service.change_password(db, user, data.current_password, data.new_password, data.confirm_password)
    return success_response(data=None, message="Password updated")

@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    return success_response(data=None, message="Logged out")