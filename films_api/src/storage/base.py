from abc import abstractmethod


class BaseStorage:
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int):
        pass

    @abstractmethod
    async def get_data_by_id(self, id: str):
        pass
