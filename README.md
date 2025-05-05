# 🏥 API RESTful - Centro Médico

API RESTful para la gestión de citas médicas desarrollada con **Python (Flask)** y **PostgreSQL**.

**Workflow Postman en archivo postman_workflow_api_medica.md**
---

## 🚀 Tecnologías Utilizadas

- Python 3  
- Flask  
- Flask SQLAlchemy  
- PostgreSQL  
- Pytest  
- Postman (para pruebas)

---

## ⚙️ Instalación

1. **Clonar el repositorio o descomprimir .zip del correo:**
```bash
git clone https://github.com/michael-urzua-y/centro_medico.git
cd centro_medico
```

2. **Crear un entorno virtual:**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. **Configurar la base de datos:**

- Crear una base de datos llamada 'medic_api'.
- Ejecutar el script 'init_db.sql' para crear las tablas necesarias.

4. **Actualizar la URI de conexión en 'app/__init__.py':**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devpass@localhost/medic_api'
```

5. **Configurar variables de entorno:**

- Renombrar '.env.example' a '.env'.
- Copiar y pegar la Stripe Secret Key proporcionada el correo.

6. **Ejecutar la aplicación:**
```bash
python run.py
```

---

## ✅ Pruebas Unitarias

Para ejecutar los tests:
```bash
PYTHONPATH=./ pytest -v
```

Las pruebas están en 'test/' e incluyen:

- Solo creación de cita (test_nueva_cita_creada)
- Creación + Pago (test_pago_exitoso)
- Creación + Pago + Confirmación (test_confirmar_cita)
- Creación + Rechazo (test_rechazar_cita_pendiente - descomentar para usar)

---

## 🔐 Autenticación

- Realiza login en '/api/auth/login' para obtener un token JWT.
- En las demás rutas protegidas, añade el token en el encabezado:

---

## 📌 Endpoints Principales

### 1. Iniciar Sesión
**POST** '/api/auth/login'
```json
{
  "email": "usuario@ejemplo.com",
  "password": "1234"
}
```

---

### 2. Pedir Cita
**POST** '/api/citas/pedir'
  - Crea una nueva cita (solo para pacientes autenticados).

```json
{
  "medico_id": 2,
  "fecha": "2025-05-02",
  "hora": "10:00"
}
```

---

### 3. Realizar Pago
**POST** '/api/pagos/realizar'
  - Registra el pago de una cita.
  - Solo pacientes pueden pagar citas propias.

```json
{
  "cita_id": 10,
  "monto": 45000,
  "payment_method_id": "pm_card_visa"
}
```

---

### 4. Verificar Pago
**GET** '/api/pagos/verificar/1'
  - Verifica el estado de un pago, en este caso el numero final 1 corresponde a pago_id

---

### 5. Confirmar Cita (Médico)
**POST** '/api/citas/confirmar'
  - Confirma una cita médica (solo médicos pueden confirmar las suyas).
```json
{
  "cita_id": 2
}
```

---

### 6. Rechazar Cita (Médico)
**POST** '/api/citas/rechazar'
  - Permite al médico autenticado rechazar una cita que le pertenece.
  - Solo se pueden rechazar citas que estén en estado 'pendiente'.
```json
{
  "cita_id": 2
}
```

---

### 7. Listar Citas del Día
**GET** '/api/citas/dia?fecha=2025-05-02'  
**GET** '/api/citas/dia?medico_id=2'
  - Lista las citas del día actual o fecha específica (solo médicos).

---

### 8. Historial del Paciente
**GET** '/api/citas/paciente?fecha=2025-05-02'  
**GET** '/api/citas/paciente'
  - Muestra el historial de citas de un paciente.
  - Puede filtrar por fecha o mostrar todas por defecto.

---

## 🧠 Funciones Clave

- **'pedir_cita()'**: Agenda una nueva cita validando fecha y disponibilidad.  
- **'realizar_pago()'**: Registra el pago de la cita pendiente del paciente autenticado.  
- **'verificar_pago()'**: Consulta el estado actual de un pago.  
- **'confirmar_cita()'**: Permite al médico confirmar citas pagadas que le corresponden.  
- **'rechazar_cita()'**: Permite al médico rechazar citas pendientes que le corresponden.  
- **'citas_del_dia()'**: Lista las citas del día o una fecha específica del médico autenticado.  
- **'citas_por_paciente()'**: Historial de citas del paciente autenticado, opcionalmente filtrado por fecha.

---

