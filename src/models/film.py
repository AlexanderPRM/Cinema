#Ранее вы уже создавали модель Film в api/v1/films.py, 
#но она используется исключительно для представления данных по HTTP. 
#Внутренние модели, одну из которых вы создаёте сейчас, 
#используется только в рамках бизнес-логики.

import orjson
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel

def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()

class ConfigMixin(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class Film(BaseModel, ConfigMixin):
    id: str
    title: str
    description: str

class Genres(BaseModel, ConfigMixin):
    id: str
    name: str
    description: str

class Actors(BaseModel, ConfigMixin):
    id: str
    full_name: str

class Writers(BaseModel, ConfigMixin):
    id: str
    full_name: str

class Directors(BaseModel, ConfigMixin):
    id: str
    full_name: str

