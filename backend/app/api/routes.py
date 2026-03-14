from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.celery_app import celery_app
from app.models.schemas import SearchInput, SearchResultEnvelope, SearchStartResponse, SearchStatus
from app.tasks.search_task import execute_search

router = APIRouter(prefix="/api/v1", tags=["search"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/search", response_model=SearchStartResponse)
@limiter.limit(settings.rate_limit)
def start_search(request: Request, payload: SearchInput) -> SearchStartResponse:
    if settings.require_consent and not payload.consent_confirmed:
        raise HTTPException(status_code=400, detail="consent_confirmed must be true")

    if not any([payload.username, payload.email, payload.phone, payload.full_name, payload.photo_url]):
        raise HTTPException(status_code=400, detail="At least one identifier is required")

    task = execute_search.delay(payload.model_dump(mode="json"))
    return SearchStartResponse(task_id=task.id, status="PENDING")


@router.get("/search/{task_id}", response_model=SearchResultEnvelope)
def get_search_result(task_id: str) -> SearchResultEnvelope:
    task = AsyncResult(task_id, app=celery_app)
    status = SearchStatus(task.status)

    if status == SearchStatus.SUCCESS:
        return SearchResultEnvelope(task_id=task_id, status=status, result=task.result)

    if status == SearchStatus.FAILURE:
        return SearchResultEnvelope(task_id=task_id, status=status, error=str(task.result))

    return SearchResultEnvelope(task_id=task_id, status=status)
