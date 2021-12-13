from fastapi import APIRouter
from fastapi import status

from api.domain.models import ErrorResponseModel
from api.domain.models import ResponseModel
from api.domain.services.logo_service import LogoService

logo_router = APIRouter()
logo_service = LogoService()


@logo_router.get("/get", response_description="Get all supported logos", status_code=status.HTTP_200_OK)
async def get_all_logos():
    try:
        logos = logo_service.get_all_logos()
        response_model = ResponseModel(
            data=logos if logos else [],
            code=200,
            message="Logos retrieved successfully"
        )
        return response_model

    except Exception as ex:
        return ErrorResponseModel(
            error=ex.__class__.__name__,
            code=500,
            message=str(ex.args)
        )


@logo_router.get("/get/{name}", response_description="Get logo by name", status_code=status.HTTP_200_OK)
async def get_by_name(name):
    try:
        logo = logo_service.get_logo_by_name(name)
        response_model = ResponseModel(
            data=[logo] if logo else [],
            code=200 if logo else 404,
            message="Logos by name retrieved successfully" if logo else "Logo not found"
        )
        return response_model

    except Exception as ex:
        return ErrorResponseModel(
            error=ex.__class__.__name__,
            code=500,
            message=str(ex.args)
        )


@logo_router.delete("/delete/{name}", response_description="Delete logo by name", status_code=status.HTTP_200_OK)
async def delete_logo_by_name(name):
    try:
        logo_service.delete_logo_by_name(name)
        response_model = ResponseModel(
            data=[],
            code=200,
            message="Logos deleted successfully"
        )
        return response_model

    except Exception as ex:
        return ErrorResponseModel(
            error=ex.__class__.__name__,
            code=500,
            message=str(ex.args)
        )
