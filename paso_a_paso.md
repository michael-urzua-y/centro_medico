### ** CREAR BD CON TABLAS E INSERTAR USUARIOS ** ###

### INICIAR SESIÓN COMO PACIENTE
http://localhost:5000/api/auth/login
POST
{
   "email": "alberto.guerra@gmail.com",
   "password": "1234"
}

# 109b28908f59545545deea2497a90fd2

### PEDIR CITA
http://127.0.0.1:5000/api/citas/pedir
POST
+ TOKEN
{
  "medico_id": 2,
  "fecha": "2025-05-04",
  "hora": "08:15"
}

### PAGAR CITA
http://localhost:5000/api/pagos/realizar
POST
+ TOKEN
{
  "cita_id": 11,
  "monto": 45000,
  "payment_method_id": "pm_card_visa"
}

### VERIFICAR PAGO
GET http://localhost:5000/api/pagos/verificar/1

### MOSTRAR CITAS DEL PACIENTE
GET http://localhost:5000/api/citas/paciente // TODAS LAS CITAS
GET http://localhost:5000/api/citas/paciente?fecha=2025-05-02 // CITAS POR FECHA
+ TOKEN

### INICIAR SESIÓN COMO MEDICO
POST http://localhost:5000/api/auth/login
{
  "email": "marta.herrera@gmail.com",
  "password": "1234"
}

# 711cbcd0958b723d1163d10e6254823b

### LISTAR CITAS DEL MEDICO POR FECHA 
GET http://localhost:5000/api/citas/dia?fecha=2025-05-01 // BUSCAR POR FECHA
GET http://localhost:5000/api/citas/dia?medico_id=2  // BUSCAR POR ID DEL MEDICO DIA ACTUAL
+ TOKEN

### CONFIRMAR CITA MEDICA
http://localhost:5000/api/citas/confirmar
POST
+ TOKEN

{
  "cita_id": 11
}

### RECHAZAR CITA MEDICA
http://localhost:5000/api/citas/rechazar
POST
+ TOKEN

{
  "cita_id": 6
}












