import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Rate limiting: 60 req/user/min in production, relaxed in test so agents
# can run full scenario suites without hitting limits (see spec SEC-08).
RATE_LIMIT = "600/minute" if ENVIRONMENT == "test" else "60/minute"

limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])

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
    # SEC-16: Production must never return stack traces or verbose error detail.
    if ENVIRONMENT == "test":
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
