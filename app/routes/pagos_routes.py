from flask import Blueprint, request, jsonify
from app import db
from app.models import Cita, Pago
from decimal import Decimal
from app.utils.auth import token_required
from dotenv import load_dotenv
import stripe
import os


load_dotenv() 
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

pagos_bp = Blueprint('pagos', __name__, url_prefix='/api/pagos')

# Métodos de pago de prueba (Stripe 2024)
METODOS_PAGO_PRUEBA = {
    'pm_card_visa': 'Visa (4242)',
    'pm_card_mastercard': 'Mastercard (5555)',
    'pm_card_amex': 'Amex (3782)',
    'pm_card_chargeDeclined': 'Tarjeta declinada',
    'pm_card_cvcFail': 'Error CVC'
}

@pagos_bp.route('/realizar', methods=['POST'])
@token_required
def realizar_pago():
    """
    Procesa pagos con Stripe usando tokens de prueba.
    Body requerido:
    {
        "cita_id": 10,
        "monto": 45000,
        "payment_method_id": "pm_card_visa"
    }
    """
    data = request.get_json()
    paciente = request.usuario_actual

    # Validación de rol
    if paciente.rol != "paciente":
        return jsonify({"error": "Solo pacientes pueden realizar pagos"}), 403

    try:
        cita_id = data["cita_id"]
        monto = Decimal(str(data["monto"]))
        payment_method_id = data["payment_method_id"]
    except (KeyError, ValueError) as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400

    # Validar método de pago
    if payment_method_id not in METODOS_PAGO_PRUEBA:
        return jsonify({
            "error": "Método de pago no válido",
            "metodos_permitidos": list(METODOS_PAGO_PRUEBA.keys())
        }), 400

    # Validar monto positivo
    if monto <= 0:
        return jsonify({"error": "El monto debe ser mayor que cero"}), 400

    # Validar cita
    cita = Cita.query.get(cita_id)
    if not cita:
        return jsonify({"error": "La cita no existe"}), 404
    if cita.paciente_id != paciente.usuario_id:
        return jsonify({"error": "No autorizado para pagar esta cita"}), 403
    if cita.estado != "pendiente":
        return jsonify({"error": "La cita ya fue pagada/cancelada"}), 400

    # Verificar pago duplicado
    if Pago.query.filter_by(cita_id=cita_id, estado="completado").first():
        return jsonify({"error": "Esta cita ya tiene un pago completado"}), 409

    try:
        # Crear PaymentIntent en Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(monto * 100),  # Stripe usa centavos
            currency='clp',
            payment_method=payment_method_id,
            confirm=True,
            automatic_payment_methods={
                'enabled': True,
                'allow_redirects': 'never'
            },
            metadata={
                "cita_id": cita_id,
                "paciente_id": paciente.usuario_id
            }
        )

        # Registrar pago en la base de datos
        pago = Pago(
            cita_id=cita_id,
            monto=monto,
            estado="completado" if intent.status == 'succeeded' else "pendiente",
            id_pago_stripe=intent.id,
            metodo_pago=METODOS_PAGO_PRUEBA[payment_method_id]  # Usamos el nuevo campo
        )
        
        if intent.status == 'succeeded':
            cita.estado = "pagada"
        
        db.session.add(pago)
        db.session.commit()

        return jsonify({
            "mensaje": "Pago procesado exitosamente",
            "estado": intent.status,
            "pago_id": pago.pago_id,
            "stripe_payment_id": intent.id,
            "metodo_pago": pago.metodo_pago
        }), 200

    except stripe.error.CardError as e:
        db.session.rollback()
        return jsonify({
            "error": "Error en la tarjeta",
            "detalle": e.user_message,
            "codigo": e.code
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno",
            "detalle": str(e)
        }), 500
    

@pagos_bp.route('/verificar/<int:pago_id>', methods=['GET'])
@token_required
def verificar_pago(pago_id):
    # Verifica el estado de un pago
    try:
        pago = Pago.query.options(db.joinedload(Pago.cita)).get_or_404(pago_id)
    except:
        return jsonify({"error": f"No existe un pago con cita_id {pago_id}"}), 404 
    
    # Verificar que el pago pertenece al paciente
    if not pago.cita or pago.cita.paciente_id != request.usuario_actual.usuario_id:
        return jsonify({"error": "No autorizado"}), 403

    return jsonify({
        "pago_id": pago.pago_id,
        "estado": pago.estado,
        "stripe_payment_id": pago.id_pago_stripe,
        "cita_id": pago.cita_id,
        "monto": float(pago.monto),
        "fecha": pago.fecha_creada.isoformat(),
        "metodo_pago": pago.metodo_pago
    }), 200