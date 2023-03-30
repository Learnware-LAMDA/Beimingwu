from flask import Blueprint, jsonify, request
from config import C

user_api = Blueprint("User-API", __name__)

@user_api.route("/")
def index():
    C.stats += 1
    return f"User API Index {C.stats}"