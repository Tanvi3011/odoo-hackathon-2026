import os
from datetime import date

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ForbiddenException, NotFoundException, ValidationException
from app.models.attendance import Attendance
from app.models.user import User
from app.schemas.user import AdminUserUpdate, EmployeeCard, UserProfile, UserUpdate


async def get_employee_cards(db: AsyncSession) -> list[EmployeeCard]:
    result = await db.execute(select(User).where(User.is_active == True))
    users = result.scalars().all()
    cards = []
    today = date.today()
    for user in users:
        attendance = (
            await db.execute(
                select(Attendance).where(
                    Attendance.employee_id == user.employee_id,
                    Attendance.date == today,
                )
            )
        ).scalar_one_or_none()
        status = attendance.status if attendance else "absent"
        cards.append(
            EmployeeCard(
                employee_id=user.employee_id,
                first_name=user.first_name,
                last_name=user.last_name,
                department=user.department,
                designation=user.designation,
                profile_picture=user.profile_picture,
                status=status,
            )
        )
    return cards


async def get_profile(db: AsyncSession, employee_id: str, requester: User) -> UserProfile:
    if requester.role == "employee" and requester.employee_id != employee_id:
        raise ForbiddenException("Cannot view other employee profiles")
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("Employee not found")
    return UserProfile.model_validate(user)


async def update_profile(db: AsyncSession, employee_id: str, data: UserUpdate | AdminUserUpdate, requester: User) -> UserProfile:
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("Employee not found")
    if requester.role == "employee" and requester.employee_id != employee_id:
        raise ForbiddenException("Cannot edit other employee profiles")

    update_data = data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return await get_profile(db, employee_id, requester)


async def upload_avatar(db: AsyncSession, employee_id: str, file: UploadFile) -> str:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise ValidationException("Only .jpg, .jpeg, .png allowed")

    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:
        raise ValidationException("Max file size is 2MB")

    ext = "jpg" if file.content_type == "image/jpeg" else "png"
    filename = f"{employee_id}.{ext}"
    filepath = f"uploads/avatars/{filename}"

    os.makedirs("uploads/avatars", exist_ok=True)
    with open(filepath, "wb") as avatar_file:
        avatar_file.write(contents)

    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("Employee not found")
    user.profile_picture = f"/uploads/avatars/{filename}"
    await db.commit()
    return user.profile_picture


async def delete_employee(db: AsyncSession, employee_id: str):
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("Employee not found")
    user.is_active = False
    await db.commit()
