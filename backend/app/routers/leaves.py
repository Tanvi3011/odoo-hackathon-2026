from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin, require_employee
from app.models.user import User
from app.schemas.leave import LeaveAction, LeaveApply
from app.services import leave_service
from app.utils import success_response

router = APIRouter(prefix="/api/v1/leaves", tags=["Leaves"])


@router.post("/apply")
async def apply_leave(data: LeaveApply, db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    response = await leave_service.apply_leave(db, user.employee_id, data)
    return success_response(data=response.model_dump(), message="Leave applied")


@router.get("/my")
async def get_my_leaves(status: str | None = Query(None), db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    leaves = await leave_service.get_my_leaves(db, user.employee_id)
    if status:
        leaves = [leave for leave in leaves if leave.status == status]
    return success_response(data=[leave.model_dump() for leave in leaves], message="Leaves fetched")


@router.get("/")
async def get_all_leaves(
    status: str | None = Query(None),
    employee_id: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    leaves = await leave_service.get_all_leaves(db, status, employee_id)
    return success_response(data=[leave.model_dump() for leave in leaves], message="Leaves fetched")


@router.put("/{request_id}")
async def process_leave(
    request_id: str,
    action: LeaveAction,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    response = await leave_service.process_leave(db, request_id, admin.employee_id, action)
    return success_response(data=response.model_dump(), message="Leave processed")


@router.get("/balance")
async def get_balance(db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    balance = await leave_service.get_balance(db, user.employee_id)
    return success_response(data=balance, message="Balance fetched")
