import pytest
import random  # Import para generar valores aleatorios
from app import create_app
from app.models import Cita, Usuario
from datetime import datetime, timedelta, UTC

@pytest.fixture(scope="module")
def client():
    app = create_app(test_config={
        "TESTING": True,
        "DISABLE_AUTH": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://devuser:devpass@localhost/medic_api",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

@pytest.fixture(scope="module")
def nueva_cita(client):
    """
        Este fixture central crea una nueva cita médica que puede ser usada en múltiples tests.
        La cita generada sirve como base para probar diferentes flujos:
        - Solo creación de cita (test_nueva_cita_creada)
        - Creación + Pago (test_pago_exitoso)
        - Creación + Pago + Confirmación (test_confirmar_cita)
        - Creación + Rechazo (test_rechazar_cita_pendiente - descomentar para usar)
    """
    with client.application.app_context():
        paciente = Usuario.query.filter_by(rol="paciente").first()
        medico = Usuario.query.filter_by(rol="medico").first()
        assert medico is not None, "No se encontró un médico en la base de datos"

    token = paciente.token

    # Usando random para evitar conflictos con horarios duplicados
    data = {
        "medico_id": medico.usuario_id,
        "fecha": (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%d"),
        "hora": f"10:{random.randint(10, 59):02d}"  # Hora aleatoria entre 10:10 y 10:59
    }

    response = client.post("/api/citas/pedir",
                         json=data,
                         headers={
                             "Content-Type": "application/json",
                             "Authorization": f"Bearer {token}"
                         })
    
    assert response.status_code in [200, 201]
    cita_data = response.get_json()
    return cita_data['cita_id']

def test_nueva_cita_creada(nueva_cita):
    assert nueva_cita is not None


def test_pago_exitoso(client, nueva_cita):
    paciente = Usuario.query.filter_by(rol="paciente").first()
    token = paciente.token

    data = {
        "cita_id": nueva_cita,
        "monto": 45000,  # CLP
        "payment_method_id": "pm_card_visa"
    }

    response = client.post('/api/pagos/realizar',
                           json=data,
                           headers={
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}"
                           })

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response["estado"] == "succeeded"
    assert "pago_id" in json_response
    assert "stripe_payment_id" in json_response


def test_confirmar_cita(client, nueva_cita):
    medico = Usuario.query.filter_by(rol="medico").first()
    token = medico.token

    data = {
        "cita_id": nueva_cita
    }

    response = client.post('/api/citas/confirmar',
                           json=data,
                           headers={
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}"
                           })

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response["mensaje"] == "Cita confirmada correctamente"
    assert json_response["cita_id"] == nueva_cita


# def test_rechazar_cita_pendiente(client, nueva_cita):
#     medico = Usuario.query.filter_by(rol="medico").first()
#     data = {"cita_id": nueva_cita}
#     token = medico.token
#     response = client.post('/api/citas/rechazar', 
#                          json=data,
#                          headers={
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {token}'
#         })
       
#     assert response.status_code == 200
#     assert b'rechazada' in response.data.lower()