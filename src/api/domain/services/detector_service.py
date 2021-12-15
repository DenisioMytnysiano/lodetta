import os
from dataclasses import dataclass
from functools import lru_cache
from typing import List, NoReturn

import numpy as np
import torch
from PIL import Image
from dotenv import load_dotenv

from api.data_access.dao.logo_dao import LogoDao
from api.data_access.data_sources.data_source_factory import DataSourceFactory
from api.data_access.data_sources.gdrive_data_source import GoogleDriveDataSource
from api.domain.models.bbox_model import BboxModel
from api.domain.models.detect_request_model import DetectRequestModel
from api.domain.models.image_model import ImageModel
from api.domain.models.prediction_model import PredictionModel
from api.domain.models.weights_import_model import WeightsImportModel
from api.extensions.utils import get_logger

load_dotenv()
model_weights = os.environ.get("MODEL")
logger = get_logger(__name__)


@lru_cache
def load_model():
    model = torch.hub.load('ultralytics/yolov5', "custom", path=model_weights)
    return model


logo_dao = LogoDao()


@dataclass
class DetectorService:
    model: torch.nn.Module = load_model()

    def detect(self, detection_config: DetectRequestModel) -> List[ImageModel]:
        data_source = DataSourceFactory.get_data_source(detection_config)
        files = data_source.get_the_data(detection_config.info)
        images = [Image.open(file) for file in files]
        predictions = self.model(images)
        predictions = predictions.pandas().xyxy
        classes = {
            logo.id: logo.name for logo
            in logo_dao.get_logo_by_ids(
                np.array(
                    [prediction["class"].values
                     for prediction in predictions]
                ).flatten().tolist()
            )
        }
        result = []
        for filename, prediction in zip([os.path.basename(path) for path in files], predictions):

            preds = []
            for index, row in prediction[prediction["class"].isin(classes)].iterrows():
                preds.append(
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

            result.append(
                ImageModel(
                    image_name=filename,
                    predictions=preds
                )
            )
        return result

    def import_weights(self, weights_config: WeightsImportModel) -> NoReturn:
        load_model.clear_cache()
        data_source = GoogleDriveDataSource()
        weights = data_source.get_the_data(weights_config.weights_path)
        if len(weights) > 1:
            raise Exception("Path is referencing a directory, not a model file.")
        self.model = torch.hub.load('ultralytics/yolov5', "custom", path=weights[0])
        logger.info(f"Weights from {weights_config.weights_path} loaded successfully into the model")
