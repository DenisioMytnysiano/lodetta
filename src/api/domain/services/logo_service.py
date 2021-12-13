import logging
from typing import List, Optional, NoReturn

from api.data_access.dao.logo_dao import LogoDao
from api.domain.models import LogoModel
from api.extensions.utils import get_logger

logger = get_logger(__name__)
logo_dao = LogoDao()


class LogoService:

    def get_all_logos(self) -> List[LogoModel]:
        logos = logo_dao.get_all_logos()
        logger.info(f"Retrieved {len(logos)} logos from database.")
        return logos

    def get_logo_by_name(self, logo_name: str) -> Optional[LogoModel]:
        logo = logo_dao.get_logo_by_name(logo_name)
        logger.info(f"Retrieved logo by name {logo_name} from database.")
        return logo

    def delete_logo_by_name(self, logo_name: str) -> NoReturn:
        logo_dao.delete_logo_by_name(logo_name)
        logger.info(f"Deleted logo by name {logo_name} from database.")
