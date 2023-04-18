from config import C
from flask_cors import CORS
from flask import Flask
from database import SQLite
import api
from learnware import market

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['UPLOAD_FOLDER'] = C.upload_path
CORS(app)


def main(port=8088):
    # Init database
    database = None
    if C.database_type == "sqlite":
        database = SQLite(path=C.sqlite_path)
    if database is None:
        raise ValueError(f"Database type {C.database_type} is not supproted.")
    setattr(C, "database", database)
    setattr(C, "stats", 0)

    # Init engine
    engine = None
    if C.engine_type == "easymarket":
        engine = market.EasyMarket()
    if engine is None:
        raise ValueError(f"Learnware engine type {C.engine_type} is not supproted.")
    setattr(C, "engine", engine)

    # Init flask
    app.register_blueprint(api.auth_api, url_prefix="/auth")
    app.register_blueprint(api.user_api, url_prefix="/user")
    app.register_blueprint(api.admin_api, url_prefix="/admin")
    app.register_blueprint(api.engine_api, url_prefix="/engine")
    app.run(host="0.0.0.0", port=port, threaded=True, debug=True)


if __name__ == "__main__":
    import fire
    fire.Fire(main)