import os.path

from pydub import AudioSegment  # type: ignore [import-untyped]

from app.celery import celery as app
from app.services.drive import DriveService
from app.utils.files import get_path_for_tempfile


@app.task
def trim(id_in_drive: str, start_ms: int, end_ms: int) -> str:
    _, ext = os.path.splitext(id_in_drive)

    if not ext or not ext.startswith("."):
        raise ValueError("Couldn't determinate format")

    file_temp = get_path_for_tempfile(ext)

    drive = DriveService()
    drive.get_to_file_sync(id_in_drive, file_temp)

    audio_format = ext[1:]
    audio: AudioSegment = AudioSegment.from_file(file_temp, format=audio_format)

    new_end = len(audio) - end_ms
    if (new_end - end_ms) <= 0:
        raise ValueError("Invalid length")

    trimmed = audio[start_ms:new_end]

    trimmed.export(file_temp, audio_format)
    trimmed_id_in_drive = drive.put_from_file_sync(file_temp)

    return trimmed_id_in_drive
