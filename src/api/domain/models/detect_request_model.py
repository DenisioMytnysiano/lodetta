from enum import Enum

from pydantic import BaseModel


class DataSourceType(str, Enum):
    image = "image"
    google_drive = "google_drive"


class DetectRequestModel(BaseModel):
    data_source: DataSourceType
    info: str
