from config import C
from flask_cors import CORS
from flask import Flask
from database import SQLite
import api

# import learnware.market as market

app = Flask(__name__)
app.secret_key = "my_secret_key"
CORS(app)


def main():
    # Init database
    database = None
    if C.database_type == "sqlite":
        database = SQLite(path=C.sqlite_path)
    if database is None:
        raise ValueError(f"Database type {C.database_type} is not supproted.")
    setattr(C, "database", database)
    setattr(C, "stats", 0)

    # Init engine
    # engine = None
    # if C.engine_type == "basic":
    #     engine = market.BaseMarket()
    #     engine.reload_market(C.engine_market_path, C.engine_property_path, C.engine_load_mode)
    # if engine is None:
    #     raise ValueError(f"Learnware engine type {C.engine_type} is not supproted.")
    # setattr(C, "engine", engine)

    # Init flask
    app.register_blueprint(api.auth_api, url_prefix="/auth")
    app.register_blueprint(api.user_api, url_prefix="/user")
    app.register_blueprint(api.admin_api, url_prefix="/admin")
    app.register_blueprint(api.engine_api, url_prefix="/engine")
    app.run(host="0.0.0.0", port=8088, threaded=True, debug=True)


if __name__ == "__main__":
    main()
