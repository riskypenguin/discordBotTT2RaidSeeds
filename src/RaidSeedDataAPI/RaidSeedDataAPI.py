import json
from typing import Any, Callable

import requests
from requests import Response
from src.domain.RaidSeedDataProvider import RaidSeedDataProvider
from src.model.SeedType import SeedType


class RaidSeedDataAPI(RaidSeedDataProvider):

    def __init__(self, *, base_url: str, auth_key: str) -> None:
        super().__init__()

        self.base_url = base_url
        self.auth_key = auth_key

        self.headers = {"secret": auth_key, "Accept": "application/json"}

    def _make_api_request(self,
                          *,
                          method: Callable,
                          path: str,
                          data: Any | None = None,
                          headers: dict[str, str] | None = None) -> Response:

        headers = self.headers | (headers or {})

        response = method(url=f"{self.base_url}/{path}",
                          headers=headers,
                          data=data)

        response.raise_for_status()

        return response

    def list_seed_identifiers(self: RaidSeedDataProvider,
                              *,
                              seed_type: SeedType = SeedType.RAW) -> list[str]:

        response = self._make_api_request(
            method=requests.get,
            path=f"admin/all_seed_filenames/{seed_type.value}")

        return response.json()

    def save_seed(self: RaidSeedDataProvider, *, identifier: str,
                  data: str) -> None:

        self._make_api_request(method=requests.post,
                               path=f"admin/raw_seed_file/{identifier}",
                               data=data)

    def get_seed(
        self: RaidSeedDataProvider,
        *,
        identifier: str,
        seed_type: SeedType = SeedType.RAW,
    ) -> list[Any]:

        response = self._make_api_request(
            method=requests.get,
            path=f"admin/seed_file/{seed_type.value}/{identifier}")

        return response.json()

    def delete_seed(
        self: RaidSeedDataProvider,
        *,
        identifier: str,
    ) -> None:

        self._make_api_request(method=requests.delete,
                               path=f"admin/raw_seed_file/{identifier}")
