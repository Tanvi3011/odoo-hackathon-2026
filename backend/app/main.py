import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import app.models
from app.database import Base, engine
from app.exceptions import HRMSException
from app.routers import attendance, auth, employees, leaves, payroll
from app.utils import error_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized and tables created")
    yield


app = FastAPI(title="HRMS Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads/avatars", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.exception_handler(HRMSException)
async def hrms_exception_handler(request: Request, exc: HRMSException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail, exc.detail, exc.status_code),
    )


app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(leaves.router)
app.include_router(payroll.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
