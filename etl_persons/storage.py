import abc
import json

from typing import Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path
        self.default_state = {"sync": "1999-11-19 11:11:11.111111", "stopped_uuid": []}

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path) as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w", encoding="utf8") as file:
                json.dump(self.default_state, file)
            return self.retrieve_state()

    def save_state(self, state: dict) -> None:
        data = self.retrieve_state()
        data.update(state)
        with open(self.file_path, "w", encoding="utf8") as file:
            json.dump(data, file)


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        data = self.storage.retrieve_state()
        return data.get(key, None)
