import redis


class State:
    def __init__(self, storage: redis):
        self.storage = storage

    async def set_state(self, key: str, value: str) -> None:
        await self.storage.set(key, value)

    async def get_state(self, key: str) -> str:
        return await self.storage.get(key)
