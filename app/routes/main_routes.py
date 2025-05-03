# app/routes/main_routes.py
from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"mensaje": "API de Citas Médicas funcionando correctamente"})
