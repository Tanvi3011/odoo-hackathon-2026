from pydantic import BaseModel


class SalaryStructure(BaseModel):
    monthly_wage: float
    yearly_wage: float
    basic_salary: float
    hra: float
    allowances: float
    pf_contribution: float
    professional_tax: float
    other_deductions: float
    performance_bonus: float
    gross_salary: float
    total_deductions: float
    net_salary: float


class PayrollUpdate(BaseModel):
    monthly_wage: float | None = None
    basic_salary: float | None = None
    hra: float | None = None
    allowances: float | None = None
    pf_contribution: float | None = None
    professional_tax: float | None = None
    other_deductions: float | None = None
    performance_bonus: float | None = None
