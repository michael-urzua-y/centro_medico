### ** CREAR BD CON TABLAS E INSERTAR USUARIOS ** ###

### INICIAR SESIÓN COMO PACIENTE
http://localhost:5000/api/auth/login
POST
{
   "email": "alberto.guerra@gmail.com",
   "password": "1234"
}

# f6e56703f8e6b2d63e65fa2852029332

### PEDIR CITA
http://127.0.0.1:5000/api/citas/pedir
POST
+ TOKEN
{
  "medico_id": 4,
  "fecha": "2025-05-04",
  "hora": "07:15"
}

### PAGAR CITA
http://localhost:5000/api/pagos/realizar
POST
+ TOKEN
{
  "cita_id": 6,
  "monto": 45000
}

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

# 546ced30c991c506ebdbfb641941176a

### LISTAR CITAS DEL MEDICO POR FECHA 
GET http://localhost:5000/api/citas/dia?fecha=2025-05-01 // BUSCAR POR FECHA
GET http://localhost:5000/api/citas/dia?medico_id=2  // BUSCAR POR ID DEL MEDICO DIA ACTUAL
+ TOKEN

### CONFIRMAR CITA MEDICA
http://localhost:5000/api/citas/confirmar
POST
+ TOKEN

{
  "cita_id": 2
}

### RECHAZAR CITA MEDICA
http://localhost:5000/api/citas/rechazar
POST
+ TOKEN

{
  "cita_id": 6
}












