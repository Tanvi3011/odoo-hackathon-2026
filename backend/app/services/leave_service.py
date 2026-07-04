from datetime import date, datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException, ValidationException
from app.models.leave_request import LeaveRequest
from app.models.user import User
from app.schemas.leave import LeaveAction, LeaveApply, LeaveRequestResponse


def get_business_days(start: date, end: date) -> int:
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


async def to_response(db: AsyncSession, request: LeaveRequest) -> LeaveRequestResponse:
    user = (await db.execute(select(User).where(User.employee_id == request.employee_id))).scalar_one_or_none()
    name = f"{user.first_name} {user.last_name}" if user else "Unknown"
    return LeaveRequestResponse(
        id=str(request.id),
        employee_id=request.employee_id,
        employee_name=name,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        days=request.days,
        reason=request.reason,
        status=request.status,
        admin_comment=request.admin_comment,
        requested_at=request.requested_at,
    )


async def apply_leave(db: AsyncSession, employee_id: str, data: LeaveApply) -> LeaveRequestResponse:
    if data.start_date > data.end_date:
        raise ValidationException("Start date must be before end date")
    if data.start_date < date.today():
        raise ValidationException("Cannot apply for leave in the past")

    overlap = (
        await db.execute(
            select(LeaveRequest).where(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status == "approved",
                LeaveRequest.start_date <= data.end_date,
                LeaveRequest.end_date >= data.start_date,
            )
        )
    ).scalars().all()
    if overlap:
        raise ConflictException("Leave overlaps with an approved leave")

    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("User not found")

    if data.leave_type == "paid_time_off" and user.paid_leave_balance <= 0:
        raise ValidationException("Insufficient paid leave balance")

    days = get_business_days(data.start_date, data.end_date)

    request = LeaveRequest(
        employee_id=employee_id,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        days=days,
        reason=data.reason,
        attachment_url=data.attachment_url,
    )
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return await to_response(db, request)


async def get_my_leaves(db: AsyncSession, employee_id: str) -> list[LeaveRequestResponse]:
    requests = (
        await db.execute(
            select(LeaveRequest)
            .where(LeaveRequest.employee_id == employee_id)
            .order_by(LeaveRequest.requested_at.desc())
        )
    ).scalars().all()
    return [await to_response(db, request) for request in requests]


async def get_all_leaves(
    db: AsyncSession,
    status_filter: str | None = None,
    employee_id: str | None = None,
) -> list[LeaveRequestResponse]:
    query = select(LeaveRequest)
    if status_filter:
        query = query.where(LeaveRequest.status == status_filter)
    if employee_id:
        query = query.where(LeaveRequest.employee_id == employee_id)

    requests = (await db.execute(query.order_by(LeaveRequest.requested_at.desc()))).scalars().all()
    return [await to_response(db, request) for request in requests]


async def process_leave(db: AsyncSession, request_id: str, admin_id: str, action: LeaveAction) -> LeaveRequestResponse:
    request = await db.get(LeaveRequest, int(request_id))
    if not request:
        raise NotFoundException("Leave request not found")
    if request.status != "pending":
        raise ConflictException("Leave request already processed")

    request.status = action.status
    request.admin_comment = action.admin_comment
    request.responded_at = datetime.now(timezone.utc)
    request.responded_by = admin_id

    if action.status == "approved" and request.leave_type == "paid_time_off":
        user = (await db.execute(select(User).where(User.employee_id == request.employee_id))).scalar_one_or_none()
        if user:
            user.paid_leave_balance = max(0, user.paid_leave_balance - request.days)

    await db.commit()
    await db.refresh(request)
    return await to_response(db, request)


async def get_balance(db: AsyncSession, employee_id: str) -> dict:
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("User not found")
    return {
        "paid": user.paid_leave_balance,
        "sick": user.sick_leave_balance,
        "unpaid": 0,
    }
