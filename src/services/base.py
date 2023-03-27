from abc import abstractmethod
from typing import Any


class BaseService:
    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def get_by_param(self, *args, **kwargs) -> Any:
        pass
