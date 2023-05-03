import uuid

from db.models import UserLoginHistory
from user_agents import parse


def is_uuid_valid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def check_device_type(user_agent: str):
    device_types = UserLoginHistory.DeviceType
    user_agent = parse(user_agent)
    if user_agent.is_mobile:
        user_device_type = device_types.MOBILE
    elif user_agent.is_pc:
        user_device_type = device_types.PC
    elif user_agent.is_tablet:
        user_device_type = device_types.TABLET
    elif user_agent.is_bot:
        user_device_type = device_types.BOT
    else:
        user_device_type = device_types.UNKNOWN

    return user_device_type
