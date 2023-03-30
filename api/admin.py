from flask import Blueprint, jsonify, request
from config import C

admin_api = Blueprint("Admin-API", __name__)

@admin_api.route("/")
def index():
    C.stats += 1
    return f"Admin API Index {C.stats}"