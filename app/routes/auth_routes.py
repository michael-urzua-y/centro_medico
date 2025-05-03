from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
# POST http://localhost:5000/api/auth/login
# {
#   "email": "usuario@ejemplo.com",
#   "password": "1234"
# }
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuario = Usuario.query.filter_by(email=email, password=password).first()

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar token aleatorio y guardarlo
    token = secrets.token_hex(16)
    usuario.token = token
    db.session.commit()

    return jsonify({
        "mensaje": "Login exitoso",
        "token": token,
        "usuario_id": usuario.usuario_id,
        "rol": usuario.rol
    }), 200
