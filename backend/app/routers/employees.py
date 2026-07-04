from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import AdminUserUpdate, UserUpdate
from app.services import employee_service, payroll_service
from app.utils import success_response

router = APIRouter(prefix="/api/v1/employees", tags=["Employees"])


@router.get("/")
async def get_employees(db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    cards = await employee_service.get_employee_cards(db)
    return success_response(data=[card.model_dump() for card in cards], message="Employees fetched")


@router.get("/me")
async def get_me(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    profile = await employee_service.get_profile(db, user.employee_id, user)
    data = profile.model_dump()
    if user.role in ["admin", "hr"]:
        data["salary"] = (await payroll_service.get_payroll(db, user.employee_id)).model_dump()
    return success_response(data=data, message="Profile fetched")


@router.get("/{employee_id}")
async def get_employee(employee_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    profile = await employee_service.get_profile(db, employee_id, user)
    data = profile.model_dump()
    if user.role in ["admin", "hr"]:
        data["salary"] = (await payroll_service.get_payroll(db, employee_id)).model_dump()
    return success_response(data=data, message="Profile fetched")


@router.put("/me")
async def update_me(data: UserUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    profile = await employee_service.update_profile(db, user.employee_id, data, user)
    return success_response(data=profile.model_dump(), message="Profile updated")


@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    data: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    profile = await employee_service.update_profile(db, employee_id, data, admin)
    return success_response(data=profile.model_dump(), message="Employee updated")


@router.post("/me/avatar")
async def upload_avatar(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    url = await employee_service.upload_avatar(db, user.employee_id, file)
    return success_response(data={"url": url}, message="Avatar uploaded")


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    await employee_service.delete_employee(db, employee_id)
    return success_response(data=None, message="Employee deleted")
