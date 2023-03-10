from typing import Optional

from redis.asyncio import Redis

redis: Optional[Redis] = None


# Если вы хотите подключиться к удаленному хранилищу данных Redis,
# вы можете указать хосты и номера портов с помощью флагов -h и -p. Если вы настроили аутентификацию Redis, вы можете включить флаг -a и указать ваш пароль:
# redis-cli -h host -p port_number -a password
# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    pool = redis.ConnectionPool(host='async_sprint_1_redis_1', port=6379, db=0)
    redis = redis.Redis(connection_pool=pool)
    return redis


print(get_redis().get('key'))
