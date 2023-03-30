from config import C
from flask_cors import CORS
from flask import Flask
from database import SQLite
import api

app = Flask(__name__)
CORS(app)


def main():
    # Init database
    database = None
    if C.database_type == "sqlite": database = SQLite(path=C.sqlite_path)
    if database is None:
        raise ValueError(f'Database type {C.database_type} is not supproted.')
    setattr(C, "database", database)
    setattr(C, "stats", 0)
    # Init engine
    
    # Init flask
    app.register_blueprint(api.user_api,   url_prefix="/user")
    app.register_blueprint(api.admin_api,  url_prefix="/admin")
    app.register_blueprint(api.engine_api, url_prefix="/engine")
    app.run(host='0.0.0.0', port=8088, threaded=True, debug=True)
    
if __name__ == '__main__':
    main()