from core.config import google_config
from core.utils import check_social_account, generate_random_string, normalize_email
from db.models import SocialAccount, User
from db.postgres import db
from google_auth_oauthlib import flow
from googleapiclient import discovery
from services.user_service import UserService


class GoogleProvider:
    def __init__(self) -> None:
        self.flow = flow.Flow.from_client_secrets_file(
            google_config.GOOGLE_FILE,
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ],
        )
        self.flow.redirect_uri = google_config.GOOGLE_REDIRECT_URI

    def get_auth_url(self):
        auth_url, state = self.flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        return auth_url

    def get_tokens(self, response):
        self.flow.fetch_token(authorization_response=response)
        return self.flow.credentials

    def get_service(self, creds):
        service = discovery.build(serviceName="oauth2", version="v2", credentials=creds)
        return service

    def signin(self, response, useragent):
        creds = self.get_tokens(response)
        service = self.get_service(creds)
        user_data = service.userinfo().get().execute()
        if account := check_social_account(user_data["id"], "google"):
            return account
        user = UserService()
        if (
            created_user := db.session.query(User)
            .filter_by(email=normalize_email(user_data["email"]))
            .first()
        ):
            role = user.get_user_role(created_user)
            email = created_user.email
        else:
            email, _, role, created_user = user.signup(
                user_data["email"], generate_random_string(), user_data["given_name"], useragent
            )

        social_account = SocialAccount(
            user=created_user, social_id=user_data["id"], social_name="google"
        )
        db.session.add(social_account)
        db.session.commit()
        return (created_user, email, role)


google_provider = GoogleProvider()
