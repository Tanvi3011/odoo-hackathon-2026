from datetime import date, time

from pydantic import BaseModel, ConfigDict, EmailStr


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    address: str | None
    department: str | None
    designation: str | None
    date_of_joining: date
    profile_picture: str | None
    company_name: str
    role: str


class UserUpdate(BaseModel):
    phone: str | None = None
    address: str | None = None
    profile_picture: str | None = None


class AdminUserUpdate(UserUpdate):
    first_name: str | None = None
    last_name: str | None = None
    department: str | None = None
    designation: str | None = None
    role: str | None = None
    is_active: bool | None = None
    monthly_wage: float | None = None
    yearly_wage: float | None = None
    basic_salary: float | None = None
    hra: float | None = None
    allowances: float | None = None
    pf_contribution: float | None = None
    professional_tax: float | None = None
    other_deductions: float | None = None
    performance_bonus: float | None = None
    work_start_time: time | None = None
    work_end_time: time | None = None


class EmployeeCard(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    department: str | None
    designation: str | None
    profile_picture: str | None
    status: str
