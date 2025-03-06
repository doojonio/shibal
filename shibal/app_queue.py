from celery import Celery  # type: ignore [import-untyped]
from pydub import AudioSegment  # type: ignore [import-untyped]

from app.config import settings
from app.services.drive import DriveService

app = Celery(
    "app_queue", broker=str(settings.CELERY_DSN), backend=str(settings.CELERY_DSN)
)


# TODO: tempfile to process
@app.task
def trim(id_in_drive: str, start_ms: int, end_ms: int) -> str:
    drive = DriveService()
    drive.get_to_file_sync(id_in_drive, "./tmp/to_process.wav")

    audio: AudioSegment = AudioSegment.from_file("./tmp/to_process.wav", "wav")

    new_end = len(audio) - end_ms
    if (new_end - end_ms) <= 0:
        raise ValueError("Invalid length")

    trimmed = audio[start_ms:new_end]

    trimmed.export("./tmp/trimmed.wav", "wav")
    trimmed_id_in_drive = drive.put_from_file_sync("./tmp/trimmed.wav")

    return trimmed_id_in_drive


@app.task
def cut(id_in_drive: str, start_ms: int, end_ms: int) -> str:
    drive = DriveService()
    drive.get_to_file_sync(id_in_drive, "./tmp/to_process.wav")

    audio: AudioSegment = AudioSegment.from_file("./tmp/to_process.wav", "wav")

    new_audio = audio[:start_ms] + audio[end_ms:]

    new_audio.export("./tmp/trimmed.wav", "wav")
    in_drive_id = drive.put_from_file_sync("./tmp/trimmed.wav")

    return in_drive_id
