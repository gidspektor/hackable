from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.auth_service import AuthService


class JWTMiddleware(BaseHTTPMiddleware):
	"""
	Middleware to validate JWT in the request headers.
	"""

	async def dispatch(self, request: Request, call_next):
		# Skip JWT validation for OPTIONS requests
		if request.method == "OPTIONS":
			return await call_next(request)

		# Extract the JWT from headers
		token = request.headers.get("bearer")

		if not token or not AuthService.verify_token(token):
			return JSONResponse(
				status_code=401,
				content={"detail": "Invalid token"}
			)

		# Proceed to the next request handler
		response = await call_next(request)
		return response
