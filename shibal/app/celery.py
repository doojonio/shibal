from celery import Celery  # type: ignore [import-untyped]

from app.config import settings

celery = Celery(
    "shibal", broker=str(settings.CELERY_DSN), backend=str(settings.CELERY_DSN)
)

celery.autodiscover_tasks(["app.tasks"])
