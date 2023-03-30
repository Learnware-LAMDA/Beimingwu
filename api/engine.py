from flask import Blueprint, jsonify, request
from config import C

engine_api = Blueprint("Engine-API", __name__)

@engine_api.route("/")
def index():
    C.stats += 1
    return f"Engine API Index {C.stats}"