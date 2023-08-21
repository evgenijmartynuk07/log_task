import io
from datetime import datetime


from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from log.archive_read import archive_reader
from log.db.models import DBLog


async def process_uploaded_file(file: UploadFile, db: AsyncSession) -> None:
    read_file = file.file.readlines()

    for line in read_file:
        line = line.decode("utf-8").split(" ")

        try:
            time_created = line.pop(3)[1:]
        except Exception:
            continue

        date_format = "%d/%b/%Y:%H:%M:%S"
        message = " ".join(line)

        try:
            timestamp = datetime.strptime(time_created, date_format)
        except ValueError:
            raise ValueError("""The context of this file is not supported.
            Please try next context for log file:
            Common Log Format (CLF),
            W3C Extended Log Format,
            Apache NCSA Log Format
            """)

        db_log = DBLog(timestamp=timestamp, message=message)
        db.add(db_log)
        await db.commit()


async def process_uploaded_archive(file: UploadFile, db) -> str:
    failed_files = []

    read_file = file.file.read()
    archive_format = file.filename.split(".")[-1]

    buffer = io.BytesIO(read_file)

    file_list, archive = archive_reader(buffer, archive_format)

    for file_name in file_list:

        extracted_file = archive.read(file_name)
        fake_upload_file = UploadFile(
            filename=file_name,
            file=io.BytesIO(extracted_file)
        )

        try:
            await process_uploaded_file(fake_upload_file, db)
        except ValueError:
            failed_files.append(file_name)
            continue

    archive.close()

    message = "All files were successfully uploaded to Database"
    if failed_files:
        return f"{message}, except: {failed_files}"
    return message
