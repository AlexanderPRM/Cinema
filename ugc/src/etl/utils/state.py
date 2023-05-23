import redis


class State:
    def __init__(self, storage: redis):
        self.storage = storage

    def set_state(self, key: str, value: str) -> None:
        self.storage.set(key, value)

    def get_state(self, key: str) -> str:
        return self.storage.get(key)
