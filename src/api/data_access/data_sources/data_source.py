import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from shutil import rmtree
from typing import NoReturn

from dotenv import load_dotenv

from api.extensions.utils import get_directory_size

load_dotenv()
TMP_FOLDER_PATH = os.environ.get("TMP_FOLDER")


@dataclass
class DataSource(ABC):

    @abstractmethod
    def _validate_info(self, info) -> NoReturn:
        pass

    @abstractmethod
    def _get_data_internal(self, info) -> list[str]:
        pass

    def get_the_data(self, info) -> list[str]:
        self._validate_info(info)
        self.clear_tmp_dir()
        return self._get_data_internal(info)

    def clear_tmp_dir(self):
        if os.path.exists(TMP_FOLDER_PATH):
            if get_directory_size(TMP_FOLDER_PATH) > int(os.environ.get("TMP_FOLDER_LIMIT")):
                rmtree(TMP_FOLDER_PATH)
