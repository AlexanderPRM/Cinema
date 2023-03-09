import abc
import json
import os
from time import sleep
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(state: dict) -> None:
        """Сохранить состояние в постоянное хранилище
        тут можно добавлять значения в json
        """
        pass
        # JsonFileStorage.save(state)

    @abc.abstractmethod
    def retrieve_state() -> dict:
        """
        Загрузить состояние локально из постоянного хранилища
        """
        pass


class JsonFileStorage(BaseStorage):
    """
    будет сохранять данные в формате JSON в указанный файл (file_path) и доставать данные из этого файла.
    """

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = "state.json"
        self.fname = ".data_file.json"

    def save_state(self, entry: dict):
        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode="w") as f:
                f.write(json.dumps(entry, indent=2))
                sleep(2)
        else:
            with open(self.file_path) as feedsjson:
                # feeds = json.loads(feedsjson.read())
                dic = {}
                try:
                    feeds = json.load(feedsjson)
                    for key, value in feeds.items():
                        dic[key] = value
                except:
                    pass
                for key, value in entry.items():
                    dic[key] = value
                with open(self.file_path, mode="w") as f:
                    f.write(json.dumps(dic, indent=2))

    def retrieve_state(self):
        if os.path.isfile(self.file_path):
            try:
                with open(self.file_path, mode="r") as f:
                    state = json.load(f)
                    return state
            except:
                return {}
        else:
            return {}


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        state = {key: value}
        self.storage.save_state(state)
        self.state[key] = value

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        # state = self.storage.retrieve_state(self)
        return self.state.get(key)
