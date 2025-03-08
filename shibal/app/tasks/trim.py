import os.path
from uuid import UUID

from pydub import AudioSegment  # type: ignore [import-untyped]

from app.celery import celery as app
from app.db import session
from app.models.operations import OperationTypes
from app.services.drive import DriveService
from app.services.operations import new_operation
from app.services.users import get_user_by_id
from app.utils.files import get_path_for_tempfile


@app.task
def trim(user_id: UUID, id_in_drive: str, start_ms: int, end_ms: int) -> str:
    with session() as db:
        user = get_user_by_id(db, user_id, with_for_update=True)
        with new_operation(db, user, OperationTypes.TRIM) as op:
            _, ext = os.path.splitext(id_in_drive)

            if not ext or not ext.startswith("."):
                raise ValueError("Couldn't determinate format")

            file_temp = get_path_for_tempfile(ext)

            drive = DriveService()
            drive.get_to_file_sync(id_in_drive, file_temp)

            audio_format = ext[1:]
            audio: AudioSegment = AudioSegment.from_file(file_temp, format=audio_format)

            audio_length = len(audio)
            new_end = audio_length - end_ms
            if (new_end - end_ms) <= 0:
                raise ValueError("Invalid length")

            audio = audio[start_ms:new_end]

            audio.export(file_temp, audio_format)

            op.set_details("length", audio_length)
            op.set_details("new_length", len(audio))
            op.set_details("trim_start", start_ms)
            op.set_details("trim_end", end_ms)

            trimmed_id_in_drive = drive.put_from_file_sync(file_temp)
        db.commit()

    return trimmed_id_in_drive
