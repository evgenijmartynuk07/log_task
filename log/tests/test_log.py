import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import MagicMock, patch
from main import app
from log.loging_format import process_uploaded_file, process_uploaded_archive
from fastapi import UploadFile


class MockFile(UploadFile):
    def __init__(self, content):
        self.file = io.BytesIO(content)


@pytest.mark.asyncio
async def test_process_uploaded_file_valid_data():
    fake_file_data = b'127.0.0.1 - - [20/Aug/2023:12:34:56 +0000] "GET /page HTTP/1.1" 200 1234\n'

    mock_file = MockFile(fake_file_data)
    fake_db_session = MagicMock(spec=AsyncSession)

    with patch('log.loging_format.open', return_value=mock_file):
        await process_uploaded_file(mock_file, fake_db_session)

    assert fake_db_session.add.call_count == 1
    assert fake_db_session.commit.call_count == 1


@pytest.mark.asyncio
async def test_process_uploaded_file_invalid_date():
    fake_file_data = b'127.0.0.1 - - [20/InvalidDate/2023:12:34:56 +0000] "GET /page HTTP/1.1" 200 1234\n'

    mock_file = MockFile(fake_file_data)
    fake_db_session = MagicMock(spec=AsyncSession)

    with patch('log.loging_format.open', return_value=mock_file):
        with pytest.raises(ValueError):
            await process_uploaded_file(mock_file, fake_db_session)

    assert fake_db_session.add.call_count == 0
    assert fake_db_session.commit.call_count == 0


class MockUnauthorizedUser:
    is_authenticated = False


def mock_current_not_active_user():
    return MockUnauthorizedUser()


def test_get_logs_unauthorized():
    with patch(
            'user.auth.permissions.current_active_user',
            mock_current_not_active_user
    ):
        client = TestClient(app)
        response = client.get("/logs/")

        assert response.status_code == 401

        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Unauthorized"


class MockArchive:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

    def close(self):
        pass


class MockUploadFile:
    def __init__(self, filename, uploaded_file) -> None:
        self.filename = filename
        self.file = uploaded_file

    def read(self):
        return self.file.read()


@pytest.mark.asyncio
async def test_process_uploaded_archive_success():
    fake_archive_data = b'content_of_your_archive_file_here'
    mock_archive = MockArchive(fake_archive_data)
    fake_db_session = MagicMock()

    mock_upload_file = MockUploadFile("test_archive.zip", mock_archive)

    with patch('log.loging_format.archive_reader', return_value=([], mock_archive)), \
            patch('log.loging_format.process_uploaded_file') as mock_process_uploaded_file:
        mock_process_uploaded_file.side_effect = [None, None]

        result = await process_uploaded_archive(mock_upload_file, fake_db_session)

    assert result == "All files were successfully uploaded to Database"


if __name__ == '__main__':
    pytest.main()
