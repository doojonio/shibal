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
def change_volume(user_id: UUID, id_in_drive: str, dB: int) -> str:
    with session() as db:
        user = get_user_by_id(db, user_id, with_for_update=True)
        with new_operation(db, user, OperationTypes.VOLUME) as op:
            _, ext = os.path.splitext(id_in_drive)

            if not ext or not ext.startswith("."):
                raise ValueError("Couldn't determinate format")

            file_temp = get_path_for_tempfile(ext)

            drive = DriveService()
            drive.get_to_file_sync(id_in_drive, file_temp)

            audio_format = ext[1:]
            audio: AudioSegment = AudioSegment.from_file(file_temp, audio_format)

            audio += dB

            audio.export(file_temp, "wav")

            op.set_details("dB", dB)
            op.set_details("length", len(audio))

            in_drive_id = drive.put_from_file_sync(file_temp)
        db.commit()

    return in_drive_id
