import os
from functools import lru_cache
from typing import List, NoReturn

import torch
from dotenv import load_dotenv

from api.data_access.dao.logo_dao import LogoDao
from api.domain.models.bbox_model import BboxModel
from api.domain.models.detect_request_model import DetectRequestModel
from api.domain.models.prediction_model import PredictionModel
from api.domain.models.weights_import_model import WeightsImportModel

load_dotenv()
model_weights = os.environ.get("MODEL")


@lru_cache
def load_model():
    model = torch.hub.load('ultralytics/yolov5', "custom", path=model_weights)
    return model


model = load_model()
logo_dao = LogoDao()


class DetectorService:

    def detect(self, detection_config: DetectRequestModel) -> List[PredictionModel]:
        predictions = model([detection_config.info])
        predictions = predictions.pandas().xyxy[0]
        classes = {
            logo.id: logo.name for logo
            in logo_dao.get_logo_by_ids(predictions["class"].values.tolist())
        }
        result = []

        for index, row in predictions[predictions["class"].isin(classes)].iterrows():
            result.append(
                PredictionModel(
                    class_name=classes[row["class"]],
                    confidence=row["confidence"],
                    prediction=BboxModel(
                        x_min=row["xmin"],
                        y_min=row["ymin"],
                        x_max=row["xmax"],
                        y_max=row["ymax"]
                    )
                )
            )
        return result

    def import_weights(self, weights_config: WeightsImportModel) -> NoReturn:
        pass

    def state_report(self):
        pass
