from flask_cors import CORS
from flask import Flask, jsonify
from database import SQLAlchemy
import restful
import restful.auth
import restful.user
import restful.engine
import restful.admin
from learnware import market
import context
from context import config as C
import flask_bcrypt
import flask_jwt_extended
import requests


app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['JWT_SECRET_KEY'] = app.secret_key

app.config['UPLOAD_FOLDER'] = C.upload_path
CORS(app)
bcrypt = flask_bcrypt.Bcrypt(app)
jwt = flask_jwt_extended.JWTManager(app)


@jwt.unauthorized_loader
def on_unauthorized(error_message: str) -> requests.Response:
    return jsonify({"code": 11, "msg": "Unauthorized access."}), 200
    pass


def main():
    context.init_backend()
    
    # Init database
    admin_password = flask_bcrypt.generate_password_hash('admin').decode("utf-8")

    context.init_database(admin_password)
    context.stats = 0

    # Init engine
    context.init_engine()

    # Init flask
    app.register_blueprint(restful.auth.auth_blueprint, url_prefix='/auth')
    app.register_blueprint(restful.user.user_blueprint, url_prefix='/user')
    app.register_blueprint(restful.engine.engine_blueprint, url_prefix='/engine')
    app.register_blueprint(restful.admin.admin_blueprint, url_prefix='/admin')
    
    app.run(host=C.listen_address, port=C.listen_port, threaded=True, debug=True, use_reloader=False)




if __name__ == "__main__":
    main()