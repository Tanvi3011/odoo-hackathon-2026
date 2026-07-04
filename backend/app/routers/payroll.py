from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin, require_employee
from app.models.user import User
from app.schemas.payroll import PayrollUpdate
from app.services import payroll_service
from app.utils import success_response

router = APIRouter(prefix="/api/v1/payroll", tags=["Payroll"])


@router.get("/me")
async def get_my_payroll(db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    salary = await payroll_service.get_payroll(db, user.employee_id)
    return success_response(data=salary.model_dump(), message="Payroll fetched")


@router.get("/{employee_id}")
async def get_payroll(employee_id: str, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    salary = await payroll_service.get_payroll(db, employee_id)
    return success_response(data=salary.model_dump(), message="Payroll fetched")


@router.put("/{employee_id}")
async def update_payroll(
    employee_id: str,
    data: PayrollUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    salary = await payroll_service.update_salary(db, employee_id, data)
    return success_response(data=salary.model_dump(), message="Payroll updated")


@router.post("/{employee_id}/calculate")
async def calculate_payroll(employee_id: str, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    salary = await payroll_service.get_payroll(db, employee_id)
    return success_response(data=salary.model_dump(), message="Payroll calculated")
