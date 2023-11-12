import functools
from flask import Blueprint, g, jsonify, request, session
from . import utils
import lib.database_operations as database
import flask_bcrypt
import flask_jwt_extended
import flask_restx as flask_restful
import datetime
import context
import hashlib


auth_blueprint = Blueprint("Auth-API", __name__)
api = flask_restful.Api(auth_blueprint)


def admin_login_required(view):
    @flask_jwt_extended.jwt_required()
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)

        if user["role"] < 1:
            return {"code": 12, "msg": "Admin account required."}, 200
        return view(*args, **kwargs)

    return wrapped_view


def super_admin_login_required(view):
    @flask_jwt_extended.jwt_required()
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)

        if user["role"] < 2:
            return {"code": 12, "msg": "Super Admin account required."}, 200
        return view(*args, **kwargs)

    return wrapped_view


class RegisterApi(flask_restful.Resource):
    def post(self):
        print("register api called")

        body = request.get_json()
        keys = ["username", "password", "email"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200

        username = body["username"]
        password = body["password"]
        email = body["email"]
        confirm_email = body.get("confirm_email", True)

        email_pattern_check = False
        for email_pattern in context.config["register_email_patterns"]:
            if email_pattern in email:
                email_pattern_check = True
                break
            pass

        if not email_pattern_check:
            return {"code": 41, "msg": "Your email is not allowed to register."}, 200

        password_hash = flask_bcrypt.generate_password_hash(password).decode("utf-8")

        code, msg, user_id = database.register_user(username=username, password=password_hash, email=email)

        if code != 0 and code != 53:
            return {"code": code, "msg": msg}, 200

        if confirm_email:
            # generate email verification code
            verification_code = utils.generate_email_verification_code(
                email, secret_key=context.config["app_secret_key"]
            )
            # send email
            utils.send_verification_email(email, verification_code, email_config=context.config["email"])
            pass
        else:
            database.update_email_confirm_time(email=email)
            pass

        result = {"code": code, "msg": "success", "data": {"user_id": user_id}}

        return result, 200

    pass


class ResendEmailConfirmApi(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, location="json")

    @api.expect(parser)
    def post(self):
        body = request.get_json()
        keys = ["email"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200

        email = body["email"]
        verification_code = utils.generate_email_verification_code(email, secret_key=context.config["app_secret_key"])
        utils.send_verification_email(email, verification_code, email_config=context.config["email"])

        result = {"code": 0, "msg": "success", "data": {}}

        return result, 200

    pass


class EmailConfirmApi(flask_restful.Resource):
    def post(self):
        email = request.args.get("code")
        email = utils.decode_email_verification_code(email, secret_key=context.config["app_secret_key"])

        if email is None:
            return {"code": 55, "msg": "Invalid verification code."}, 200

        user_info = database.get_user_info(by="email", value=email)

        if user_info is None:
            return {"code": 51, "msg": "Your email not exist. Please re-register"}, 200

        if user_info["email_confirm_time"] is None:
            database.update_email_confirm_time(email=email)
            pass

        return {"code": 0, "msg": "Email confirm success."}, 200
        pass


class SendResetPasswordEmailApi(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, location="json")

    @api.expect(parser)
    def post(self):
        body = request.get_json()
        keys = ["email"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200

        email = body["email"]
        user_info = database.get_user_info(by="email", value=email)
        if user_info is None:
            return {"code": 51, "msg": "Your email not exist. Please register first"}, 200
        user_id = user_info["id"]
        verification_code = utils.generate_email_verification_code(email, secret_key=context.config["app_secret_key"])
        utils.send_reset_password_email(email, verification_code, str(user_id), email_config=context.config["email"])

        result = {"code": 0, "msg": "success", "data": {}}

        return result, 200

    pass


class ResetPasswordApi(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("code", type=str, required=True, location="json")
    parser.add_argument("user_id", type=int, required=True, location="json")

    @api.expect(parser)
    def post(self):
        body = request.get_json()
        keys = ["code", "user_id"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200

        code = body["code"]
        user_id = int(body["user_id"])
        email = utils.decode_email_verification_code(code, secret_key=context.config["app_secret_key"])
        if email is None:
            return {"code": 55, "msg": "Invalid verification code."}, 200
        user_info = database.get_user_info(by="email", value=email)
        if user_info is None:
            return {"code": 51, "msg": "Your email not exist. Please register first"}, 200
        if user_info["id"] != user_id:
            return {"code": 56, "msg": "Invalid user id."}, 200

        new_password = utils.generate_random_str(8)
        md5 = hashlib.md5(new_password.encode("utf-8")).hexdigest()
        password_hash = flask_bcrypt.generate_password_hash(md5).decode("utf-8")
        flag = database.update_user_password(pwd=password_hash, by="id", value=user_id)
        if not flag:
            return {"code": 31, "msg": "Update error."}, 200

        # Return profile
        result = {"code": 0, "msg": "Reset success", "data": {"password": new_password, "md5": md5}}

        return result


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
        elif user["email_confirm_time"] is None:
            result["code"] = 54
            result["msg"] = "Email not verified."
            pass
        elif not flask_bcrypt.check_password_hash(user["password"], password):
            result["code"] = 52
            result["msg"] = "Incorrect password."
        else:
            access_token = flask_jwt_extended.create_access_token(
                identity=user["id"], expires_delta=datetime.timedelta(days=1)
            )

            result["data"] = {"token": access_token}
            pass

        return result, 200


class LogoutApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        # todo: user_id should be added to blacklist
        result = {"code": 0, "msg": "Logout success."}
        return result


login_by_token_parser = flask_restful.reqparse.RequestParser()
login_by_token_parser.add_argument("token", type=str, required=True, location="json")
login_by_token_parser.add_argument("email", type=str, required=True, location="json")


@api.route("/login_by_token")
class LoginByTokenApi(flask_restful.Resource):
    @api.expect(login_by_token_parser)
    def post(self):
        body = request.get_json()

        token = body["token"]
        email = body["email"]

        user = database.get_user_info(by="email", value=email)
        user_id = user["id"]

        tokens = database.get_user_tokens(user_id=user_id)

        if token not in tokens:
            return {"code": 53, "msg": "Invalid token."}, 200

        access_token = flask_jwt_extended.create_access_token(
            identity=user_id, expires_delta=datetime.timedelta(days=1)
        )

        result = {"code": 0, "msg": "Login success.", "data": {"token": access_token}}

        return result, 200


class GetRoleApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)
        result = {"code": 0, "msg": "Get role success.", "data": {"role": user["role"]}}
        return result, 200

    pass


api.add_resource(RegisterApi, "/register")
api.add_resource(ResendEmailConfirmApi, "/resend_email_confirm")
api.add_resource(EmailConfirmApi, "/email_confirm")
api.add_resource(SendResetPasswordEmailApi, "/send_reset_password_email")
api.add_resource(ResetPasswordApi, "/reset_password")
api.add_resource(LoginApi, "/login")
api.add_resource(LogoutApi, "/logout")
api.add_resource(GetRoleApi, "/get_role")
