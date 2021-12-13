from enum import Enum
from pydantic import BaseModel


class LogoStatus(str, Enum):
    supported = "Supported"
    unsupported = "Unsupported"


class LogoModel(BaseModel):
    id: int
    name: str
    status: LogoStatus
