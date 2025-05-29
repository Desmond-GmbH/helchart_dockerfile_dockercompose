from typing import Any, Union
from fastapi.responses import JSONResponse

def standard_response(
    success: bool, 
    title: str, 
    message: str, 
    code: int, 
    data: Union[dict, list, str, int, None] = None
) -> JSONResponse:
    return JSONResponse(
        content={
            "success": success,
            "title": title,
            "message": message,
            "code": code,
            "data": data,
        },
        status_code=code
    )
