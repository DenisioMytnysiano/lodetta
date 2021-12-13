from pydantic import BaseModel


class WeightsImportModel(BaseModel):
    weights_path: str
