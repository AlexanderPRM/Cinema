import string
import uuid
from secrets import choice as secrets_choice

from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from user_agents import parse

from core.config import config
from db.models import SocialAccount, UserLoginHistory
from db.postgres import db
from db.redis import redis_db


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


def set_tokens(resp, user, useragent, access_token, refresh_token):
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    redis_db.setex(
        str(user.id) + "_" + useragent + "_refresh",
        config.REFRESH_TOKEN_EXPIRES,
        refresh_token,
    )
    return resp


def normalize_email(email):
    email_user, email_domain = email.lower().strip().split("@")
    if "+" in email_user:
        email_user = email_user[: email_user.find("+")]
    return f"{email_user}@{email_domain}"


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets_choice(alphabet) for _ in range(16))


def check_social_account(social_id, social_name):
    account = (
        db.session.query(SocialAccount)
        .filter_by(social_id=social_id, social_name=social_name)
        .first()
    )
    if account:
        user, email, role = account.user, account.user.email, account.user.service_info.role
        return (user, email, role)
