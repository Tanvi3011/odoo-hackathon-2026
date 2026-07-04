from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException
from app.models.user import User
from app.schemas.payroll import PayrollUpdate, SalaryStructure


def calculate_salary(user: User) -> SalaryStructure:
    monthly_wage = user.monthly_wage or 0.0
    yearly_wage = monthly_wage * 12
    basic = user.basic_salary or 0.0
    hra = user.hra or 0.0
    allowances = user.allowances or 0.0
    pf = user.pf_contribution or 0.0
    pt = user.professional_tax or 0.0
    other = user.other_deductions or 0.0
    bonus = user.performance_bonus or 0.0

    gross = basic + hra + allowances + bonus
    deductions = pf + pt + other
    net = gross - deductions

    return SalaryStructure(
        monthly_wage=monthly_wage,
        yearly_wage=yearly_wage,
        basic_salary=basic,
        hra=hra,
        allowances=allowances,
        pf_contribution=pf,
        professional_tax=pt,
        other_deductions=other,
        performance_bonus=bonus,
        gross_salary=gross,
        total_deductions=deductions,
        net_salary=net,
    )


async def update_salary(db: AsyncSession, employee_id: str, data: PayrollUpdate) -> SalaryStructure:
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("User not found")

    update_data = data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    if user.monthly_wage:
        user.yearly_wage = user.monthly_wage * 12

    await db.commit()
    await db.refresh(user)
    return calculate_salary(user)


async def get_payroll(db: AsyncSession, employee_id: str) -> SalaryStructure:
    user = (await db.execute(select(User).where(User.employee_id == employee_id))).scalar_one_or_none()
    if not user:
        raise NotFoundException("User not found")
    return calculate_salary(user)
