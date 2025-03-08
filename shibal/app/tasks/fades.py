import os.path
from uuid import UUID

from pydub import AudioSegment  # type: ignore [import-untyped]

from app.celery import celery as app
from app.models.operations import OperationTypes
from app.services.drive import DriveService
from app.services.operations import new_operation
from app.services.users import get_user_by_id
from app.utils.files import get_path_for_tempfile


from app.db import session


@app.task
def add_fades(
    user_id: UUID, id_in_drive: str, fade_in_ms: int, fade_out_ms: int
) -> str:
    with session() as db:
        user = get_user_by_id(db, user_id, with_for_update=True)
        with new_operation(db, user, OperationTypes.FADES) as op:
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

            op.set_details("length", audio_len)
            op.set_details("fade_in", fade_in_ms)
            op.set_details("fade_out", fade_out_ms)

            in_drive_id = drive.put_from_file_sync(file_temp)
        db.commit()

    return in_drive_id
