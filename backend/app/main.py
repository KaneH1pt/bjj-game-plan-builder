import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Rate limiting: 60/min in production, effectively unlimited in test
_rate_limit = "60/minute" if ENVIRONMENT == "production" else "6000/minute"

limiter = Limiter(key_func=get_remote_address, default_limits=[_rate_limit])

app = FastAPI()
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # SEC-16: Production must never return stack traces or verbose error detail
    if ENVIRONMENT == "production":
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


@app.get("/health")
@limiter.exempt
async def health():
    return {"status": "ok"}
