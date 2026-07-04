from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class LeaveApply(BaseModel):
    leave_type: Literal["paid_time_off", "sick_leave", "unpaid_leave"]
    start_date: date
    end_date: date
    reason: str
    attachment_url: str | None = None


class LeaveAction(BaseModel):
    status: Literal["approved", "rejected"]
    admin_comment: str | None = None


class LeaveRequestResponse(BaseModel):
    id: str
    employee_id: str
    employee_name: str
    leave_type: str
    start_date: date
    end_date: date
    days: int
    reason: str
    status: str
    admin_comment: str | None
    requested_at: datetime
