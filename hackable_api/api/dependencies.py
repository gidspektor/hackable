from fastapi import HTTPException, Request

from services.auth_service import AuthService

async def auth_exception_handler(request: Request) -> None:
    """Validate and decode the JWT"""

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = AuthService.verify_token(auth_header.replace("Bearer ", ""))
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return token
