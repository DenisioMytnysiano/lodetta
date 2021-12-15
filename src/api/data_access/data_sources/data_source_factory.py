from api.data_access.data_sources.gdrive_data_source import GoogleDriveDataSource
from api.data_access.data_sources.url_data_source import UrlDataSource
from api.domain.models.detect_request_model import DataSourceType, DetectRequestModel, DataType


class DataSourceFactory:

    @staticmethod
    def get_data_source(data_source_type: DetectRequestModel):
        if data_source_type.data_source == DataSourceType.url:
            if data_source_type.data_type == DataType.directory:
                raise ValueError("Folder data type is not supported for url data source")
            return UrlDataSource()
        elif data_source_type.data_source == DataSourceType.google_drive:
            return GoogleDriveDataSource(is_directory=data_source_type.data_type == DataType.directory)
        else:
            raise ValueError(f"Data source {data_source_type} is not a valid data source type.")

