import string
from secrets import choice as secrets_choice

from core.config import yandex_config
from db.models import SocialAccount, User
from db.postgres import db
from services.user_service import UserService
from yandexid import YandexID, YandexOAuth


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets_choice(alphabet) for _ in range(16))


class YandexProvider:
    def __init__(self) -> None:
        self.yandex_oauth = YandexOAuth(
            client_id=yandex_config.CLIENT_ID,
            client_secret=yandex_config.CLIENT_SECRET,
            redirect_uri=yandex_config.YANDEX_REDIRECT_URI,
        )

    def get_auth_url(self):
        return self.yandex_oauth.get_authorization_url()

    def signin(self, code, useagent):
        token = self.yandex_oauth.get_token_from_code(code)
        social_user = YandexID(token.access_token)
        user_data = social_user.get_user_info_json()
        account = (
            db.session.query(SocialAccount)
            .filter_by(social_id=user_data.psuid, social_name="yandex")
            .first()
        )
        if account:
            user, email, role = account.user, account.user.email, account.user.service_info.role
            return user, email, role

        user = UserService()
        if created_user := db.session.query(User).filter_by(email=user_data.default_email).first():
            role = user.get_user_role(created_user)
            email = created_user.email
        else:
            email, _, role, created_user = user.signup(
                user_data.default_email, generate_random_string(), user_data.first_name, useagent
            )

        social_account = SocialAccount(
            user=created_user, social_id=user_data.psuid, social_name="yandex"
        )
        db.session.add(social_account)
        db.session.commit()
        return created_user, email, role


yandex_provider = YandexProvider()
