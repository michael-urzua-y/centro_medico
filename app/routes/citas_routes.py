from flask import Blueprint, request, jsonify
from app import db
from app.models import Cita, Usuario
from datetime import datetime, time, date
from app.utils.auth import token_required

citas_bp = Blueprint('citas', __name__, url_prefix='/api/citas')

# Horarios válidos de atención
def horario_valido(hora):
    mañana = time(7, 0) <= hora <= time(12, 0)
    tarde = time(14, 0) <= hora <= time(18, 0)
    return mañana or tarde

@citas_bp.route("/pedir", methods=["POST"])
# POST http://127.0.0.1:5000/api/citas/pedir
# {
#   "medico_id": 2,
#   "fecha": "2025-05-01",
#   "hora": "10:30"
# }
@token_required
def pedir_cita():
    # Permite a un paciente agendar una nueva cita médica indicando médico,fecha y hora.
    data = request.get_json()

    paciente = request.usuario_actual
    if paciente.rol != "paciente":
        return jsonify({"error": "Solo pacientes pueden pedir citas"}), 403

    try:
        medico_id = data["medico_id"]
        fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        hora = datetime.strptime(data["hora"], "%H:%M").time()
    except Exception as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400

    # Validar fecha futura
    if fecha < date.today():
        return jsonify({"error": "No se puede pedir una cita en una fecha pasada"}), 400

    if not horario_valido(hora):
        return jsonify({"error": "La hora está fuera del horario permitido (7-12 / 14-18)"}), 400

    # Validar existencia y rol del médico
    medico = Usuario.query.get(medico_id)
    if not medico or medico.rol != 'medico':
        return jsonify({"error": "El ID proporcionado no pertenece a un médico válido"}), 400

    # Validar disponibilidad del médico
    cita_existente = Cita.query.filter_by(
        medico_id=medico_id,
        fecha=fecha,
        hora=hora
    ).first()

    if cita_existente:
        return jsonify({"error": "Ya existe una cita en ese horario con este médico"}), 409

    # Crear la cita
    nueva_cita = Cita(
        paciente_id=paciente.usuario_id,
        medico_id=medico_id,
        fecha=fecha,
        hora=hora,
        estado='pendiente'
    )
    db.session.add(nueva_cita)
    db.session.commit()

    return jsonify({
        "mensaje": "Cita creada correctamente",
        "cita_id": nueva_cita.cita_id
    }), 201

@citas_bp.route("/confirmar", methods=["POST"])
# POST http://localhost:5000/api/citas/confirmar
# {
#   "cita_id": 2
# }
@token_required
def confirmar_cita():
    # Permite al médico confirmar una cita pagada que le pertenece.
    data = request.get_json()
    medico = request.usuario_actual

    if medico.rol != "medico":
        return jsonify({"error": "Solo médicos pueden confirmar citas"}), 403

    try:
        cita_id = data["cita_id"]
    except:
        return jsonify({"error": "Debe enviar el cita_id"}), 400

    cita = Cita.query.get(cita_id)

    if not cita:
        return jsonify({"error": "La cita no existe"}), 404

    if cita.medico_id != medico.usuario_id:
        return jsonify({"error": "No está autorizado para confirmar esta cita"}), 403

    if cita.estado != "pagada":
        return jsonify({"error": "Solo se pueden confirmar citas pagadas"}), 400

    cita.estado = "confirmada"
    db.session.commit()

    return jsonify({
        "mensaje": "Cita confirmada correctamente",
        "cita_id": cita.cita_id
    }), 200

@citas_bp.route("/rechazar", methods=["POST"])
# POST http://localhost:5000/api/citas/rechazar
# {
#   "cita_id": 2
# }
@token_required
def rechazar_cita():
    # Permite al médico autenticado rechazar una cita que le pertenece.
    # Solo se pueden rechazar citas que estén en estado 'pendiente'.
    
    data = request.get_json()
    medico = request.usuario_actual

    # Verifica que sea un médico
    if medico.rol != "medico":
        return jsonify({"error": "Solo médicos pueden rechazar citas"}), 403

    # Verifica que se haya enviado un cita_id
    try:
        cita_id = data["cita_id"]
    except:
        return jsonify({"error": "Debe enviar el cita_id"}), 400

    # Busca la cita
    cita = Cita.query.get(cita_id)

    if not cita:
        return jsonify({"error": "La cita no existe"}), 404

    # Verifica que la cita le pertenezca al médico autenticado
    if cita.medico_id != medico.usuario_id:
        return jsonify({"error": "No está autorizado para rechazar esta cita"}), 403

    # Solo se pueden rechazar citas pendientes
    if cita.estado != "pendiente":
        return jsonify({"error": "Solo se pueden rechazar citas pendientes"}), 400

    # Actualiza el estado de la cita
    cita.estado = "rechazada"
    db.session.commit()

    return jsonify({
        "mensaje": "Cita rechazada correctamente",
        "cita_id": cita.cita_id
    }), 200


@citas_bp.route("/dia", methods=["GET"])
# GET http://localhost:5000/api/citas/dia?fecha=2025-05-02 / Fecha especifica
# http://localhost:5000/api/citas/dia?medico_id=2 / Fecha hoy
@token_required
def citas_del_dia():
    # Devuelve todas las citas que un médico tiene
    medico = request.usuario_actual
    if medico.rol != "medico":
        return jsonify({"error": "Solo médicos pueden acceder a este recurso"}), 403

    fecha_citas = request.args.get("fecha")

    try:
        if fecha_citas:
            fecha = datetime.strptime(fecha_citas, "%Y-%m-%d").date()
        else:
            fecha = datetime.today().date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}), 400

    citas = Cita.query.filter_by(medico_id=medico.usuario_id, fecha=fecha).order_by(Cita.hora.asc()).all()

    resultado = [
        {
            "cita_id": c.cita_id,
            "paciente_id": c.paciente_id,
            "fecha": c.fecha.strftime("%Y-%m-%d"),
            "hora": c.hora.strftime("%H:%M"),
            "estado": c.estado
        }
        for c in citas
    ]

    return jsonify({
        "medico_id": medico.usuario_id,
        "fecha": fecha.strftime("%Y-%m-%d"),
        "citas": resultado
    })

@citas_bp.route("/paciente", methods=["GET"])
# GET http://localhost:5000/api/citas/paciente?fecha=2025-05-02
# http://localhost:5000/api/citas/paciente
@token_required
def citas_por_paciente():
    # Muestra el historial de citas de un paciente.
    # Puede filtrar por fecha o mostrar todas por defecto.
    paciente = request.usuario_actual

    if paciente.rol != "paciente":
        return jsonify({"error": "Solo pacientes pueden ver su historial de citas"}), 403

    fecha_citas = request.args.get("fecha")

    try:
        if fecha_citas:
            fecha = datetime.strptime(fecha_citas, "%Y-%m-%d").date()
            citas = Cita.query.filter_by(paciente_id=paciente.usuario_id, fecha=fecha).order_by(Cita.hora.asc()).all()
        else:
            citas = Cita.query.filter_by(paciente_id=paciente.usuario_id).order_by(Cita.fecha.asc(), Cita.hora.asc()).all()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}), 400

    resultado = [
        {
            "cita_id": c.cita_id,
            "medico_id": c.medico_id,
            "fecha": c.fecha.strftime("%Y-%m-%d"),
            "hora": c.hora.strftime("%H:%M"),
            "estado": c.estado
        }
        for c in citas
    ]

    return jsonify({
        "paciente_id": paciente.usuario_id,
        "total_citas": len(resultado),
        "citas": resultado
    })
