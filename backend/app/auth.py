import logging
import os

from fastapi import HTTPException, Request
from supabase import create_client

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


async def get_current_user(request: Request):
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        logger.warning(
            "Unauthenticated access attempt: ip=%s path=%s",
            request.client.host if request.client else "unknown",
            request.url.path,
        )
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header[7:]
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = client.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return {"user": response.user, "token": token}
    except HTTPException:
        raise
    except Exception:
        logger.warning(
            "Invalid token access attempt: ip=%s path=%s",
            request.client.host if request.client else "unknown",
            request.url.path,
        )
        raise HTTPException(status_code=401, detail="Not authenticated")
