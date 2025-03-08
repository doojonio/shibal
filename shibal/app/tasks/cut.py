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
def cut(user_id: UUID, file_id: str, start_ms: int, end_ms: int) -> str:
    with session() as db:
        user = get_user_by_id(db, user_id, with_for_update=True)
        with new_operation(db, user, OperationTypes.CUT) as op:
            _, ext = os.path.splitext(file_id)

            if not ext or not ext.startswith("."):
                raise ValueError("Couldn't determinate format")

            file_temp = get_path_for_tempfile(ext)

            drive = DriveService()
            drive.get_to_file_sync(file_id, file_temp)

            audio_format = ext[1:]
            audio: AudioSegment = AudioSegment.from_file(file_temp, audio_format)

            audio_length = len(audio)
            if start_ms < 0 or start_ms > end_ms or end_ms > audio_length:
                raise ValueError("Invalid length")

            new_audio = audio[:start_ms] + audio[end_ms:]

            op.set_details("length", audio_length)
            op.set_details("new_length", len(new_audio))
            op.set_details("cut", ":".join(map(str, (start_ms, end_ms))))

            new_audio.export(file_temp, audio_format)
            cutted_file_id = drive.put_from_file_sync(file_temp)

        db.commit()

    return cutted_file_id
