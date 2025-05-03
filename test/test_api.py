import pytest
from app import create_app
from app.models import Cita, Usuario
from datetime import datetime, timedelta, UTC

@pytest.fixture
def client():
    app = create_app(test_config={
        "TESTING": True,
        "DISABLE_AUTH": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://devuser:devpass@localhost/medic_api",  # Misma DB de desarrollo
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

def test_rechazar_cita_pendiente(client):
    data = {"cita_id": 6} # Usa un ID que sabes que existe en tu base de datos
    token = "546ced30c991c506ebdbfb641941176a" # Token correspondiente al medico de la cita
    response = client.post('/api/citas/rechazar', 
                         json=data,
                         headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'  # Envía el token hardcodeado
        })
       
    assert response.status_code == 200
    assert b'rechazada' in response.data.lower()



def test_pedir_cita(client):
    with client.application.app_context():
        medico = Usuario.query.filter_by(rol="medico").first()
        assert medico is not None, "No se encontró un médico en la base de datos"

    token = "f6e56703f8e6b2d63e65fa2852029332"

    data = {
        "medico_id": medico.usuario_id,
        "fecha": datetime.now(UTC).date().isoformat(),
        "hora": (datetime.now(UTC) + timedelta(hours=2)).strftime("%H:%M")
    }

    response = client.post("/api/citas/pedir",
                           json=data,
                           headers={
                               "Content-Type": "application/json",
                               "Authorization": f"Bearer {token}"
                           })
    
    assert response.status_code in [200, 201]
    assert b'cita' in response.data.lower() or b'exito' in response.data.lower()