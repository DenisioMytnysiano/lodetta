from fastapi import APIRouter
from starlette import status

from api.domain.models import ResponseModel, ErrorResponseModel
from api.domain.models.detect_request_model import DetectRequestModel
from api.domain.models.weights_import_model import WeightsImportModel
from api.domain.services.detector_service import DetectorService

detector_router = APIRouter()
detector_service = DetectorService()


@detector_router.post("/predict", response_description="Detect logo on various data sources",
                      status_code=status.HTTP_200_OK)
async def predict(detect_config: DetectRequestModel):
    try:
        predictions = detector_service.detect(detect_config)
        response_model = ResponseModel(
            data=predictions if predictions else [],
            code=200,
            message="Detections done successfully"
        )
        return response_model

    except Exception as ex:
        return ErrorResponseModel(
            error=ex.__class__.__name__,
            code=500,
            message=str(ex.args)
        )


@detector_router.post("/import-weights", response_description="Import weights to the model",
                      status_code=status.HTTP_200_OK)
async def import_weights(weights_config: WeightsImportModel):
    try:
        detector_service.import_weights(weights_config)
        response_model = ResponseModel(
            data=[],
            code=200,
            message="Weights imported successfully"
        )
        return response_model

    except Exception as ex:
        return ErrorResponseModel(
            error=ex.__class__.__name__,
            code=500,
            message=str(ex.args)
        )
