import datetime
import uuid

from db.postgres import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(155), nullable=True)
    service_info = db.relationship("ServiceUser", backref="users", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"


class UsersRoles(db.Model):
    __tablename__ = "users_roles"
    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    name = db.Column(db.String(55), nullable=False, unique=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class ServiceUser(db.Model):
    __tablename__ = "users_service"
    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    user = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = db.Column(db.ForeignKey("users_roles.id", ondelete="CASCADE"), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __repr__(self):
        return f"<User {self.user} User Role {self.role}>"


class UserLoginHistory(db.Model):
    __tablename__ = "users_login_history"
    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    user = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    authentication_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User {self.user} User Agent {self.user_agent}>"
