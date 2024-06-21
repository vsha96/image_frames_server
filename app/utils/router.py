from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    A simple health check.
    """
    return {"message": "pong"}
