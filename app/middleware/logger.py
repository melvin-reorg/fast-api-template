"""Middleware for logging incoming requests"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Response:
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": {"method": request.method, "url": str(request.url)},
                "res": {
                    "status_code": response.status_code,
                },
            },
        )
        return response
