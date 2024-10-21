from fastapi import APIRouter

router = APIRouter()

ENDPOINT = "/health"


@router.get(ENDPOINT, response_model=dict, summary="Application Health Check")
async def application_healthcheck() -> str:
    return "Healthy"
