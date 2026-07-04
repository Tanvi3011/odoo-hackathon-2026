from datetime import date, datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, ValidationException
from app.models.attendance import Attendance
from app.models.user import User
from app.schemas.attendance import AttendanceCalendarDay, AttendanceRecord


async def check_in(db: AsyncSession, employee_id: str) -> Attendance:
    today = date.today()
    record = (
        await db.execute(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date == today,
            )
        )
    ).scalar_one_or_none()
    if record and record.check_in:
        raise ConflictException("Already checked in")
    if not record:
        record = Attendance(employee_id=employee_id, date=today)
        db.add(record)
    record.check_in = datetime.utcnow()
    record.status = "present"
    await db.commit()
    await db.refresh(record)
    return record


async def check_out(db: AsyncSession, employee_id: str) -> Attendance:
    today = date.today()
    record = (
        await db.execute(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date == today,
            )
        )
    ).scalar_one_or_none()
    if not record or not record.check_in:
        raise ValidationException("Must check in first")
    record.check_out = datetime.utcnow()
    hours = (record.check_out - record.check_in).total_seconds() / 3600
    record.work_hours = round(hours, 2)
    record.status = "half_day" if hours < 4 else "present"
    await db.commit()
    await db.refresh(record)
    return record


async def get_attendance(db: AsyncSession, employee_id: str, start: date, end: date) -> list[AttendanceRecord]:
    result = await db.execute(
        select(Attendance)
        .where(
            Attendance.employee_id == employee_id,
            Attendance.date >= start,
            Attendance.date <= end,
        )
        .order_by(Attendance.date.desc())
    )
    records = result.scalars().all()

    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    name = f"{user.first_name} {user.last_name}" if user else "Unknown"

    return [
        AttendanceRecord(
            employee_id=record.employee_id,
            employee_name=name,
            date=record.date,
            check_in=record.check_in,
            check_out=record.check_out,
            work_hours=record.work_hours,
            status=record.status,
        )
        for record in records
    ]


async def get_all_attendance(db: AsyncSession, start: date, end: date, status_filter: str | None = None) -> list[AttendanceRecord]:
    query = select(Attendance).where(Attendance.date >= start, Attendance.date <= end)
    if status_filter:
        query = query.where(Attendance.status == status_filter)

    result = await db.execute(query.order_by(Attendance.date.desc()))
    records = result.scalars().all()

    result = []
    for record in records:
        user = (await db.execute(select(User).where(User.employee_id == record.employee_id))).scalar_one_or_none()
        name = f"{user.first_name} {user.last_name}" if user else "Unknown"
        result.append(
            AttendanceRecord(
                employee_id=record.employee_id,
                employee_name=name,
                date=record.date,
                check_in=record.check_in,
                check_out=record.check_out,
                work_hours=record.work_hours,
                status=record.status,
            )
        )
    return result


async def get_calendar_month(db: AsyncSession, employee_id: str, year: int, month: int) -> list[AttendanceCalendarDay]:
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year, month, 31)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    records = (
        await db.execute(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
        )
    ).scalars().all()

    record_map = {record.date: record for record in records}
    calendar = []
    current = start_date
    while current <= end_date:
        record = record_map.get(current)
        if current.weekday() >= 5:
            status = "weekend"
        elif record:
            status = record.status
        else:
            status = "absent"

        calendar.append(
            AttendanceCalendarDay(
                date=current,
                status=status,
                check_in=record.check_in.strftime("%H:%M") if record and record.check_in else None,
                check_out=record.check_out.strftime("%H:%M") if record and record.check_out else None,
            )
        )
        current += timedelta(days=1)
    return calendar
