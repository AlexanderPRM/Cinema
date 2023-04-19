import json

from flask import Response, abort


class HttpExceptions:
    def not_exists(self, model, id):
        return abort(Response(json.dumps({"message": f"{model} {id} doesn't exists."}), 422))

    def already_exists(self, model, email):
        return abort(Response(json.dumps({"message": f"{model} {email} already exists."}), 422))

    def email_error(self):
        return abort(Response(json.dumps({"message": "Email is not correct."}), 422))

    def not_valid_uuid(self):
        return abort(Response(json.dumps({"message": "UUID is not valid."}), 422))

    def password_error(self):
        return abort(Response(json.dumps({"message": "Incorrect password."}), 401))
