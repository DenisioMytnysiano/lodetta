import os
from dataclasses import dataclass
from shutil import copyfileobj
from typing import NoReturn
from urllib.request import urlopen

from api.data_access.data_sources.data_source import DataSource

TMP_FOLDER_PATH = os.environ.get("TMP_FOLDER")


@dataclass
class UrlDataSource(DataSource):
    def _validate_info(self, url) -> NoReturn:
        pass

    def _get_data_internal(self, url) -> list[str]:
        file_path = os.path.join(TMP_FOLDER_PATH, self.__get_filename_from_url(url))
        if not os.path.exists(TMP_FOLDER_PATH):
            os.makedirs(TMP_FOLDER_PATH)
        with urlopen(url) as in_stream, open(file_path, 'wb+') as out_file:
            copyfileobj(in_stream, out_file)
        return [file_path]

    def __get_filename_from_url(self, url):
        return url.split("/")[-1]
