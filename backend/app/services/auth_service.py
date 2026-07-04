from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, ForbiddenException, UnauthorizedException, ValidationException
from app.models.company_config import CompanyConfig
from app.models.user import User
from app.schemas.auth import UserRegister
from app.utils.id_generator import generate_employee_id
from app.utils.password import generate_temp_password, hash_password, verify_password


async def register_employee(db: AsyncSession, data: UserRegister) -> tuple[User, str]:
    existing = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if existing:
        raise ConflictException("Email already registered")

    employee_id = await generate_employee_id(db, data.company_name, data.first_name, data.last_name)
    temp_password = generate_temp_password()

    config = (await db.execute(select(CompanyConfig).limit(1))).scalar_one_or_none()
    paid_balance = config.annual_paid_leave if config else 20
    sick_balance = config.annual_sick_leave if config else 10

    user = User(
        employee_id=employee_id,
        email=data.email,
        password_hash=hash_password(temp_password),
        role=data.role,
        company_name=data.company_name,
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        department=data.department,
        designation=data.designation,
        date_of_joining=data.date_of_joining,
        paid_leave_balance=paid_balance,
        sick_leave_balance=sick_balance,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user, temp_password


async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise UnauthorizedException("Invalid email or password")
    if not user.is_active:
        raise ForbiddenException("Account is deactivated")
    return user


async def change_password(db: AsyncSession, user: User, current: str | None, new: str, confirm: str):
    if new != confirm:
        raise ValidationException("Passwords do not match")

    if (
        len(new) < 8
        or not any(char.isupper() for char in new)
        or not any(char.islower() for char in new)
        or not any(char.isdigit() for char in new)
    ):
        raise ValidationException("Password must be at least 8 characters, with 1 uppercase, 1 lowercase, and 1 digit")

    if not user.first_login:
        if not current or not verify_password(current, user.password_hash):
            raise UnauthorizedException("Current password is incorrect")

    user.password_hash = hash_password(new)
    user.first_login = False
    await db.commit()
