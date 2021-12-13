from pydantic import BaseModel

from api.domain.models.bbox_model import BboxModel


class PredictionModel(BaseModel):
    class_name: str
    confidence: float
    prediction: BboxModel
