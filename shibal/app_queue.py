from celery import Celery  # type: ignore [import-untyped]
from pydub import AudioSegment  # type: ignore [import-untyped]

from app.config import settings
from app.services.drive import DriveService

app = Celery(
    "app_queue", broker=str(settings.CELERY_DSN), backend=str(settings.CELERY_DSN)
)


@app.task
def trim_start(drive_url: str, trim_millisec: int) -> str:
    drive = DriveService()
    drive.get_to(drive_url, "./tmp/to_process.wav")

    audio: AudioSegment = AudioSegment.from_file("./tmp/to_process.wav", "wav")

    if (len(audio) - trim_millisec) <= 0:
        raise ValueError("Invalid length")

    trimmed = audio[trim_millisec:]

    trimmed.export("./tmp/trimmed.wav", "wav")
    drive.put_from("trimmed_in_drive.wav", "./tmp/trimmed.wav")

    return "trimmed_in_drive.wav"
