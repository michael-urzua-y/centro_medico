
# 🏥 Flujo API Centro Medico - Postman

## 🛠️ Preparación Inicial
### Crear Base de Datos con Tablas e Insertar Usuarios  
_Este paso es previo a usar la API y se asume ya ejecutado._

---

## 🔐 1. Iniciar Sesión como Paciente
**POST** 'http://localhost:5000/api/auth/login'  
```json
{
  "email": "alberto.guerra@gmail.com",
  "password": "1234"
}
```

📌 **Guardar Token**:  
Ej : 9862b420e258b6359bd20c8228fade20'

---

## 📅 2. Pedir Cita
**POST** 'http://localhost:5000/api/citas/pedir'  
🔑 **Token Requerido**
```json
{
  "medico_id": 2,
  "fecha": "2025-05-05",
  "hora": "17:15"
}
```

---

## 💳 3. Pagar Cita
**POST** 'http://localhost:5000/api/pagos/realizar'  
🔑 **Token Requerido**
```json
{
  "cita_id": 1,
  "monto": 45000,
  "payment_method_id": "pm_card_visa"
}
```

---

## ✅ 4. Verificar Pago
**GET** 'http://localhost:5000/api/pagos/verificar/1'  
🔑 **Token Requerido**

---

## 📖 5. Ver Citas del Paciente  
🔑 **Token Requerido**

- Todas las citas:  
  **GET** 'http://localhost:5000/api/citas/paciente'

- Citas por fecha:  
  **GET** 'http://localhost:5000/api/citas/paciente?fecha=2025-05-02'

---

## 👨‍⚕️ 6. Iniciar Sesión como Médico
**POST** 'http://localhost:5000/api/auth/login'  
```json
{
  "email": "marta.herrera@gmail.com",
  "password": "1234"
}
```

📌 **Guardar Token**:  
Ej: '20d4d18fef31a81e980b9418702cce41'

---

## 📋 7. Listar Citas del Médico  
🔑 **Token Requerido**

- Por fecha específica:  
  **GET** 'http://localhost:5000/api/citas/dia?fecha=2025-05-01'

- Por médico (día actual):  
  **GET** 'http://localhost:5000/api/citas/dia?medico_id=2'

---

## ☑️ 8. Confirmar Cita
**POST** 'http://localhost:5000/api/citas/confirmar'  
🔑 **Token Requerido**
```json
{
  "cita_id": 1
}
```

---

## ❌ 9. Rechazar Cita
**POST** 'http://localhost:5000/api/citas/rechazar'  
🔑 **Token Requerido**
```json
{
  "cita_id": 1
}
```