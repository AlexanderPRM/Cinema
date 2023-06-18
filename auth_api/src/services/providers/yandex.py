from core.config import yandex_config
from core.utils import (
    check_social_account,
    generate_random_string,
    normalize_email,
    send_confirmation_email,
)
from db.models import SocialAccount, User
from db.postgres import db
from services.providers.base import OAuthSignIn
from services.user_service import UserService
from yandexid import YandexID, YandexOAuth


class YandexProvider(OAuthSignIn):
    def __init__(self) -> None:
        super(YandexProvider, self).__init__("yandex")
        self.yandex_oauth = YandexOAuth(
            client_id=yandex_config.YANDEX_CLIENT_ID,
            client_secret=yandex_config.YANDEX_CLIENT_SECRET,
            redirect_uri=yandex_config.YANDEX_REDIRECT_URI,
        )

    def get_auth_url(self):
        return self.yandex_oauth.get_authorization_url()

    def signin(self, code, useragent):
        token = self.yandex_oauth.get_token_from_code(code)
        social_user = YandexID(token.access_token)
        user_data = social_user.get_user_info_json()
        if account := check_social_account(user_data.psuid, "yandex"):
            return account

        user = UserService()
        if (
            created_user := db.session.query(User)
            .filter_by(email=normalize_email(user_data.default_email))
            .first()
        ):
            role = user.get_user_role(created_user)
            email = created_user.email
        else:
            email, _, role, created_user = user.signup(
                user_data.default_email,
                generate_random_string(),
                user_data.first_name,
                useragent,
                send_confirmation_email(normalize_email(user_data.default_email), user),
            )

        social_account = SocialAccount(
            user=created_user, social_id=user_data.psuid, social_name="yandex"
        )
        db.session.add(social_account)
        db.session.commit()
        return (created_user, email, role)


yandex_provider = YandexProvider()
