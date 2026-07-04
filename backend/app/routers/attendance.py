from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin, require_employee
from app.models.user import User
from app.services import attendance_service
from app.utils import success_response

router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])


def _serialize_attendance_record(record) -> dict:
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "date": record.date,
        "check_in": record.check_in,
        "check_out": record.check_out,
        "work_hours": record.work_hours,
        "status": record.status,
        "remarks": record.remarks,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }


@router.post("/check-in")
async def check_in(db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    record = await attendance_service.check_in(db, user.employee_id)
    return success_response(data=_serialize_attendance_record(record), message="Checked in")


@router.post("/check-out")
async def check_out(db: AsyncSession = Depends(get_db), user: User = Depends(require_employee)):
    record = await attendance_service.check_out(db, user.employee_id)
    return success_response(data=_serialize_attendance_record(record), message="Checked out")


@router.get("/me")
async def get_my_attendance(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_employee),
):
    records = await attendance_service.get_attendance(db, user.employee_id, start_date, end_date)
    return success_response(data=[record.model_dump() for record in records], message="Attendance fetched")


@router.get("/me/calendar")
async def get_my_calendar(
    year: int = Query(...),
    month: int = Query(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_employee),
):
    calendar = await attendance_service.get_calendar_month(db, user.employee_id, year, month)
    return success_response(data=[day.model_dump() for day in calendar], message="Calendar fetched")


@router.get("/")
async def get_all_attendance(
    start_date: date = Query(...),
    end_date: date = Query(...),
    employee_id: str | None = Query(None),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if employee_id:
        records = await attendance_service.get_attendance(db, employee_id, start_date, end_date)
    else:
        records = await attendance_service.get_all_attendance(db, start_date, end_date, status)
    return success_response(data=[record.model_dump() for record in records], message="Attendance fetched")


@router.get("/summary")
async def get_summary(date: date = Query(...), db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    records = await attendance_service.get_all_attendance(db, date, date)
    summary = {
        "present": len([record for record in records if record.status == "present"]),
        "absent": len([record for record in records if record.status == "absent"]),
        "half_day": len([record for record in records if record.status == "half_day"]),
        "leave": len([record for record in records if record.status == "leave"]),
    }
    return success_response(data=summary, message="Summary fetched")
