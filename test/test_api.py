import pytest
from app import create_app,  db
from app.models import Cita, Usuario

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
    
    print(response.data)  # Para debug
    
    assert response.status_code == 200
    assert b'rechazada' in response.data.lower()
