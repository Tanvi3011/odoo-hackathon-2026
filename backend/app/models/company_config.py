from datetime import time

from sqlalchemy import JSON, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CompanyConfig(Base):
    __tablename__ = "company_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String, default="Default Company")
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    working_days: Mapped[list[str]] = mapped_column(
        JSON,
        default=lambda: ["monday", "tuesday", "wednesday", "thursday", "friday"],
    )
    default_work_start: Mapped[time] = mapped_column(Time, default=time(9, 0))
    default_work_end: Mapped[time] = mapped_column(Time, default=time(18, 0))
    employee_id_counter: Mapped[int] = mapped_column(Integer, default=0)
    annual_paid_leave: Mapped[int] = mapped_column(Integer, default=20)
    annual_sick_leave: Mapped[int] = mapped_column(Integer, default=10)
