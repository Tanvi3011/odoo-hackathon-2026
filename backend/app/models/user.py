from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="employee")
    company_name: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    profile_picture: Mapped[str | None] = mapped_column(String, nullable=True)
    department: Mapped[str | None] = mapped_column(String, nullable=True)
    designation: Mapped[str | None] = mapped_column(String, nullable=True)
    date_of_joining: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    first_login: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    monthly_wage: Mapped[float | None] = mapped_column(Float, nullable=True)
    yearly_wage: Mapped[float | None] = mapped_column(Float, nullable=True)
    basic_salary: Mapped[float | None] = mapped_column(Float, nullable=True)
    hra: Mapped[float | None] = mapped_column(Float, nullable=True)
    allowances: Mapped[float | None] = mapped_column(Float, nullable=True)
    pf_contribution: Mapped[float | None] = mapped_column(Float, nullable=True)
    professional_tax: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_deductions: Mapped[float | None] = mapped_column(Float, nullable=True)
    performance_bonus: Mapped[float | None] = mapped_column(Float, nullable=True)

    work_start_time: Mapped[time] = mapped_column(Time, default=time(9, 0))
    work_end_time: Mapped[time] = mapped_column(Time, default=time(18, 0))

    paid_leave_balance: Mapped[int] = mapped_column(Integer, default=0)
    sick_leave_balance: Mapped[int] = mapped_column(Integer, default=0)
