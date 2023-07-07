import functools
from flask import Blueprint, g, jsonify, request, session
from .utils import *
import lib.database_operations as database
import flask_bcrypt
import flask_jwt_extended
import flask_restful
import datetime


auth_blueprint = Blueprint("Auth-API", __name__)
api = flask_restful.Api(auth_blueprint)


def admin_login_required(view):
    @flask_jwt_extended.jwt_required()
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)

        if user["role"] != 1:
            return {"code": 12, "msg": "Admin account required."}, 200
        return view(*args, **kwargs)

    return wrapped_view


class RegisterApi(flask_restful.Resource):
    def post(self):
        print('register api called')

        body = request.get_json()
        keys = ["username", "password", "email"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        username = body["username"]
        password = body["password"]
        email = body["email"]

        password_hash = flask_bcrypt.generate_password_hash(password).decode("utf-8")

        code, msg, user_id = database.register_user(username=username, password=password_hash, email=email)

        result = {"code": code, "msg": msg, "data": {"user_id": user_id} }

        return result, 200


class LoginApi(flask_restful.Resource):
    def post(self):
        body = request.get_json()
        keys = ["email", "password"]

        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        email = body["email"]
        password = body["password"]

        # Try to login
        result = {"code": 0, "msg": "Login success."}

        user = database.get_user_info(by="email", value=email)

        if user is None:
            result["code"] = 51
            result["msg"] = "Account not exist."
            pass

        elif not flask_bcrypt.check_password_hash(user["password"], password):
            result["code"] = 52
            result["msg"] = "Incorrect password."
        else:
            access_token = flask_jwt_extended.create_access_token(
                identity=user["id"], expires_delta=datetime.timedelta(days=1))
            
            result['data'] = {'token': access_token}
            pass

        return result, 200     


class LogoutApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        # todo: user_id should be added to blacklist
        result = {"code": 0, "msg": "Logout success."}
        return result


class GetRoleApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)
        result = {"code": 0, "msg": "Get role success.", "data": {"role": user["role"]}}
        return result, 200
    pass


api.add_resource(RegisterApi, "/register")
api.add_resource(LoginApi, "/login")
api.add_resource(LogoutApi, "/logout")
api.add_resource(GetRoleApi, "/get_role")