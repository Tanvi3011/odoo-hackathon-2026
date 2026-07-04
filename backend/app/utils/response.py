from datetime import datetime
from typing import Any

def success_response(data: Any, message: str = "Operation completed") -> dict:
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def error_response(error: str, details: str, status_code: int) -> dict:
    return {
        "success": False,
        "error": error,
        "details": details,
        "statusCode": status_code
    }