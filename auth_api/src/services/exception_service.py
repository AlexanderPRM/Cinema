import json
from http import HTTPStatus

from flask import Response, abort


class HttpExceptions:
    def not_exists(self, model, id):
        return abort(
            Response(
                json.dumps({"message": f"{model} {id} doesn't exists."}),
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        )

    def already_exists(self, model, email):
        return abort(
            Response(
                json.dumps({"message": f"{model} {email} already exists."}),
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        )

    def email_error(self):
        return abort(
            Response(
                json.dumps({"message": "Email is not correct."}),
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        )

    def not_valid_uuid(self):
        return abort(
            Response(
                json.dumps({"message": "UUID is not valid."}),
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        )

    def password_error(self):
        return abort(
            Response(
                json.dumps({"message": "Incorrect password."}),
                HTTPStatus.UNAUTHORIZED,
            )
        )
