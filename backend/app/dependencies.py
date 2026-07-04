from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.database import get_db
from app.utils.jwt import decode_token
from app.exceptions import UnauthorizedException, ForbiddenException

# This tells FastAPI to show the "Authorize" button and expect a Bearer token
security = HTTPBearer()

async def get_current_user(
    request: Request, 
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    employee_id = payload.get("sub")
    if not employee_id:
        raise UnauthorizedException("Invalid token payload")
        
    result = await db.execute(select(User).where(User.employee_id == employee_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")
        
    if user.first_login and request.url.path != "/api/v1/auth/change-password":
        raise ForbiddenException("Please change your password first")
        
    return user

async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role not in ["admin", "hr"]:
        raise ForbiddenException("Admin/HR access required")
    return user

async def require_employee(user: User = Depends(get_current_user)) -> User:
    if user.role != "employee":
        raise ForbiddenException("Employee access required")
    return user