from fastapi import HTTPException, Request

from services.auth_service import AuthService

async def auth_exception_handler(request: Request) -> None:
    """Validate and decode the JWT"""

    token = AuthService.verify_token(request.get("Authorization"))

    if not token:
        raise HTTPException(status_code=401, detail="Authorization error")

    return token
