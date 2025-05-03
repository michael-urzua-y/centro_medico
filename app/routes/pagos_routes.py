from flask import Blueprint, request, jsonify
from app import db
from app.models import Cita, Pago
from decimal import Decimal
from app.utils.auth import token_required


# Aquí defines el blueprint ANTES de usarlo
pagos_bp = Blueprint('pagos', __name__, url_prefix='/api/pagos')

@pagos_bp.route('/realizar', methods=['POST'])
# POST http://localhost:5000/api/pagos/realizar
# {
#   "cita_id": 3,
#   "monto": 10000
# }

@token_required
def realizar_pago():
    # Registra el pago de una cita si es del paciente autenticado y está pendiente.
    data = request.get_json()

    paciente = request.usuario_actual

    if paciente.rol != "paciente":
        return jsonify({"error": "Solo pacientes pueden realizar pagos"}), 403

    try:
        cita_id = data["cita_id"]
        monto = Decimal(str(data["monto"]))
    except Exception as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400

    if monto <= 0:
        return jsonify({"error": "El monto debe ser mayor que cero"}), 400

    cita = Cita.query.get(cita_id)
    if not cita:
        return jsonify({"error": "La cita no existe"}), 404

    #Validar que la cita le pertenezca al paciente autenticado
    if cita.paciente_id != paciente.usuario_id:
        return jsonify({"error": "No está autorizado para pagar esta cita"}), 403

    if cita.estado != "pendiente":
        return jsonify({"error": "La cita ya fue pagada, confirmada o rechazada"}), 400

    pago_existente = Pago.query.filter_by(cita_id=cita_id, estado="completado").first()
    if pago_existente:
        return jsonify({"error": "Esta cita ya ha sido pagada"}), 409

    pago = Pago(
        cita_id=cita_id,
        monto=monto,
        estado="completado"
    )

    cita.estado = "pagada"
    db.session.add(pago)
    db.session.commit()

    return jsonify({
        "mensaje": "Pago realizado correctamente",
        "pago_id": pago.pago_id
    }), 201
