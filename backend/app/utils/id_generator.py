from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company_config import CompanyConfig


async def generate_employee_id(db: AsyncSession, company_name: str, first_name: str, last_name: str) -> str:
    config = (await db.execute(select(CompanyConfig).limit(1))).scalar_one_or_none()
    if not config:
        config = CompanyConfig(company_name=company_name)
        db.add(config)
        await db.commit()
        await db.refresh(config)

    config.employee_id_counter += 1
    await db.commit()
    await db.refresh(config)
    seq = config.employee_id_counter

    company_part = company_name.upper()[:2] if company_name else "XX"
    first_part = first_name.upper()[0] if first_name else "X"
    last_part = last_name.upper()[0] if last_name else "X"
    year = datetime.utcnow().year

    return f"{company_part}{first_part}{last_part}{year}{seq:04d}"
