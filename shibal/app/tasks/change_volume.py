import os.path

from pydub import AudioSegment  # type: ignore [import-untyped]

from app.celery import celery as app
from app.services.drive import DriveService
from app.utils.files import get_path_for_tempfile


@app.task
def change_volume(id_in_drive: str, change_in_dB: int) -> str:
    _, ext = os.path.splitext(id_in_drive)

    if not ext or not ext.startswith("."):
        raise ValueError("Couldn't determinate format")

    file_temp = get_path_for_tempfile(ext)

    drive = DriveService()
    drive.get_to_file_sync(id_in_drive, file_temp)

    audio_format = ext[1:]
    audio: AudioSegment = AudioSegment.from_file(file_temp, audio_format)

    audio += change_in_dB

    audio.export(file_temp, "wav")
    in_drive_id = drive.put_from_file_sync(file_temp)

    return in_drive_id
