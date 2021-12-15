from pydantic import BaseModel

from api.domain.models.prediction_model import PredictionModel


class ImageModel(BaseModel):
    image_name: str
    predictions: list[PredictionModel]