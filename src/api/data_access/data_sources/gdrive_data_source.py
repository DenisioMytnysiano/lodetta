import io
import os
from dataclasses import dataclass
from typing import NoReturn

from apiclient import errors
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload

from api.data_access.data_sources.data_source import DataSource
from api.extensions.google_drive import get_google_drive_service
from api.extensions.utils import get_logger

load_dotenv()
drive_service = get_google_drive_service()
logger = get_logger(__name__)


@dataclass
class GoogleDriveDataSource(DataSource):
    is_directory: bool

    def _validate_info(self, url) -> NoReturn:
        pass

    def _get_data_internal(self, url) -> list[str]:
        files = []
        if self.is_directory:
            folder_id = self.__extract_folder_id_from_url(url)
            for file_id in self.__list_files_in_folder(folder_id):
                files.append(self.__download_file(file_id))
        else:
            file_id = self.__extract_file_id_from_url(url)
            files.append(self.__download_file(file_id))
        return files

    def __extract_file_id_from_url(self, url: str):
        return url.split("/")[-2]

    def __extract_folder_id_from_url(self, url):
        return url.split("/")[-1]

    def __download_file(self, file_id) -> str:
        files_service = drive_service.files()
        request = files_service.get_media(fileId=file_id)
        file = files_service.get(fileId=file_id).execute()
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.info(f"Downloading {file_id} %d%%." % int(status.progress() * 100))

        fh.seek(0)
        file_path = os.path.join(os.environ.get("TMP_FOLDER"), file["name"])
        if not os.path.exists(os.environ.get("TMP_FOLDER")):
            os.makedirs(os.environ.get("TMP_FOLDER"))
        with open(file_path, "wb") as f:
            f.write(fh.read())
        return file_path

    def __list_files_in_folder(self, folder_id) -> list[str]:
        files = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                children = drive_service.files().list(
                    q=f"'{folder_id}' in parents", spaces='drive', **param).execute()

                for child in children.get('files', []):
                    files.append(child['id'])
                page_token = children.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError as error:
                logger.error('An error occurred: %s' % error)
                break
        return files
