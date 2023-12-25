from flask_cors import CORS
from flask import Flask, jsonify
from database import SQLAlchemy
import restful
import restful.auth
import restful.user
import restful.engine
import restful.admin
import restful.datasets
from learnware import market
import context
from context import config as C
import flask_bcrypt
import flask_jwt_extended
from flaskext.markdown import Markdown
import requests
import hashlib
import threading
from datetime import timedelta
from lib import redis_utils
import logging
from flask.logging import default_handler


app = Flask(__name__)
app.secret_key = C.app_secret_key
app.config["JWT_SECRET_KEY"] = app.secret_key
app.config["UPLOAD_FOLDER"] = C.upload_path
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024 * 16
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3)


CORS(app)
bcrypt = flask_bcrypt.Bcrypt(app)
jwt = flask_jwt_extended.JWTManager(app)
Markdown(app)


@jwt.unauthorized_loader
def on_unauthorized(error_message: str) -> requests.Response:
    return jsonify({"code": 11, "msg": "Unauthorized access."}), 200
    pass


def main():
    context.init_backend()

    # Init database
    admin_password = "admin"
    admin_password_hash = hashlib.md5(admin_password.encode("utf-8")).hexdigest()
    admin_password_encrypt = flask_bcrypt.generate_password_hash(admin_password_hash).decode("utf-8")

    context.init_database(admin_password_encrypt)
    context.stats = 0

    # Init engine
    context.init_engine()

    # Init logger
    context.init_logger(target="file")

    # Init redis
    context.init_redis()
    sub_thread = threading.Thread(target=redis_utils.subscribe)
    sub_thread.start()

    # Init sensitive words
    context.init_sensitive_words()

    # Init flask
    app.register_blueprint(restful.auth.auth_blueprint, url_prefix="/auth")
    app.register_blueprint(restful.user.user_blueprint, url_prefix="/user")
    app.register_blueprint(restful.engine.engine_blueprint, url_prefix="/engine")
    app.register_blueprint(restful.admin.admin_blueprint, url_prefix="/admin")
    app.register_blueprint(restful.datasets.datasets_blueprint, url_prefix="/datasets")

    app.run(host=C.listen_address, port=C.listen_port, threaded=True, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
