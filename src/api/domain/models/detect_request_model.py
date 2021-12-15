from enum import Enum

from pydantic import BaseModel


class DataSourceType(str, Enum):
    url = "url"
    google_drive = "google_drive"


class DataType(str, Enum):
    standalone_file = "standalone_file"
    directory = "folder"


class DetectRequestModel(BaseModel):
    data_source: DataSourceType
    data_type: DataType
    info: str
