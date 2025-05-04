# API RESTful - Centro Médico

Esta es una API RESTful para la gestión de citas médicas desarrollada con **Python (Flask)** y **PostgreSQL**
---

## Tecnologías utilizadas

- Python 3
- Flask
- Flask SQLAlchemy
- PostgreSQL
- pytest
- Postman (para pruebas)

---


## Instalación

1. **Clonar el repositorio:**

   git clone https://github.com/michael-urzua-y/centro_medico.git
   cd centro_medico

2. **Crear un entorno virtual:**

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

3. **Configurar la base de datos:**
  
  - Crea una base de datos llamada 'medic_api'.
  - Ejecuta el script 'init_db.sql' para inicializar las tablas y datos necesarios. 

4. **Configurar la URI de conexión en `app/__init__.py`:**

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devpass@localhost/medic_api'

5. **Ejecutar:**

    python run.py

---

## Pruebas Unitarias

Para ejecutar las pruebas unitarias:

```bash
PYTHONPATH=./ pytest -v
```

Las pruebas se encuentran en la carpeta 'test/' e incluyen casos para:

- Creación de citas
- Rechazo de citas
- Autenticación de usuarios

## Autenticación por token

- Usar '/api/auth/login' para obtener un token.
- En las demás rutas, enviar el token en el header:

---

## Endpoints disponibles

### 1. POST /api/auth/login
Inicia sesión y retorna un token.
POST http://localhost:5000/api/auth/login
{
  "email": "usuario@ejemplo.com",
  "password": "1234"
}

---

### 2. POST /api/citas/pedir
Crea una nueva cita (solo para pacientes autenticados).
POST http://127.0.0.1:5000/api/citas/pedir
{
  "medico_id": 2,
  "fecha": "2025-05-02",
  "hora": "10:00"
}

---

### 3. POST /api/pagos/realizar
Registra el pago de una cita. Solo pacientes pueden pagar citas propias.
POST http://localhost:5000/api/pagos/realizar
{
  "cita_id": 10,
  "monto": 45000,
  "payment_method_id": "pm_card_visa"
}

---

### 4. POST /api/citas/confirmar
Confirma una cita médica (solo médicos pueden confirmar las suyas).
POST http://localhost:5000/api/citas/confirmar

{
  "cita_id": 2
}

---

### 5. POST /api/citas/rechazar
Permite al médico autenticado rechazar una cita que le pertenece.
Solo se pueden rechazar citas que estén en estado 'pendiente'.
POST http://localhost:5000/api/citas/rechazar

{
  "cita_id": 2
}

---

### 6. GET /api/citas/dia?fecha=YYYY-MM-DD
Lista las citas del día actual o fecha específica (solo médicos).

GET http://localhost:5000/api/citas/dia?fecha=2025-05-02  / Fecha especifica
http://localhost:5000/api/citas/dia?medico_id=2  / Fecha hoy

---

###  6. GET /api/citas/paciente?fecha=YYYY-MM-DD
Muestra el historial de citas de un paciente.
Puede filtrar por fecha o mostrar todas por defecto.

GET http://localhost:5000/api/citas/paciente?fecha=2025-05-02
http://localhost:5000/api/citas/paciente

---

## Descripción de funciones clave (documentación interna)

- pedir_cita()
  - Permite a un paciente agendar una nueva cita.
  - Valida horario, fecha y que no esté ocupada.

- realizar_pago()
  - Registra el pago de una cita si es del paciente autenticado y está pendiente.

- verificar_pago():
  - Verifica el estado de un pago

- confirmar_cita()
  - Permite al médico confirmar una cita pagada que le pertenece.

- rechazar_cita()
  - Esta función permite a un médico autenticado rechazar una cita que está asignada a él, siempre que la cita esté en estado "pendiente".

- citas_del_dia()
  - Muestra todas las citas del día (o fecha específica) para el médico autenticado.

- citas_por_paciente()
  - Lista el historial de citas del paciente autenticado.
  - Puede filtrar por fecha opcional.

---
