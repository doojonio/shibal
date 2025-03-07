import os.path

from pydub import AudioSegment  # type: ignore [import-untyped]

from app.celery import celery as app
from app.services.drive import DriveService
from app.utils.files import get_path_for_tempfile


@app.task
def add_fades(id_in_drive: str, fade_in_ms: int, fade_out_ms: int) -> str:
    _, ext = os.path.splitext(id_in_drive)

    if not ext or not ext.startswith("."):
        raise ValueError("Couldn't determinate format")

    file_temp = get_path_for_tempfile(ext)

    drive = DriveService()
    drive.get_to_file_sync(id_in_drive, file_temp)

    audio_format = ext[1:]
    audio: AudioSegment = AudioSegment.from_file(file_temp, audio_format)

    audio_len = len(audio)
    if any((ms < 0 or ms > audio_len for ms in (fade_in_ms, fade_out_ms))):
        raise ValueError("Invalid length")

    audio = audio.fade_in(fade_in_ms).fade_out(fade_out_ms)

    audio.export(file_temp, "wav")
    in_drive_id = drive.put_from_file_sync(file_temp)

    return in_drive_id
