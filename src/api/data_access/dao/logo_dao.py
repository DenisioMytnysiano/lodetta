from typing import List, Optional, NoReturn

from pymongo.collection import Collection

from api.database.utils import get_collection
from api.domain.models import LogoModel, LogoStatus

datasource: Collection = get_collection("logos")


class LogoDao:

    def get_all_logos(self) -> List[LogoModel]:
        logos = datasource.find({"status": LogoStatus.supported})
        return [LogoModel.parse_obj(logo) for logo in logos]

    def get_logo_by_name(self, logo_name: str) -> Optional[LogoModel]:
        logo = datasource.find_one({"name": logo_name, "status": LogoStatus.supported})
        return LogoModel.parse_obj(logo) if logo else None

    def get_logo_by_ids(self, ids: list[int]) -> List[LogoModel]:
        logos = datasource.find({"id": {"$in": ids}, "status": LogoStatus.supported})
        return [LogoModel.parse_obj(logo) for logo in logos]

    def delete_logo_by_name(self, logo_name: str) -> NoReturn:
        datasource.update_one(
            {"name": logo_name},
            {"$set": {
                "status": LogoStatus.unsupported,
            }}
        )
