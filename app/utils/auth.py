from functools import wraps
from flask import request, jsonify
from app.models import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        # Extraer el token si viene con "Bearer ...":
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

        usuario = Usuario.query.filter_by(token=token).first()
        if not usuario:
            return jsonify({"error": "Token inválido"}), 403

        request.usuario_actual = usuario
        return f(*args, **kwargs)

    return decorated
