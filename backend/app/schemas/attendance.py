from datetime import date, datetime

from pydantic import BaseModel


class AttendanceRecord(BaseModel):
    employee_id: str
    employee_name: str
    date: date
    check_in: datetime | None
    check_out: datetime | None
    work_hours: float
    status: str


class AttendanceCalendarDay(BaseModel):
    date: date
    status: str
    check_in: str | None
    check_out: str | None
