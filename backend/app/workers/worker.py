from app.core.celery_app import celery_app

# Import tasks so Celery registers them.
from app.tasks import search_task as _search_task  # noqa: F401

__all__ = ["celery_app"]
