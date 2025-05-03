from app import db
#     Representa una cita médica entre un paciente y un médico.

class Cita(db.Model):
    __tablename__ = 'citas'
    __table_args__ = {'schema': 'centro_medico'}

    cita_id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('centro_medico.usuarios.usuario_id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('centro_medico.usuarios.usuario_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String, nullable=False)  # pendiente, pagada, confirmada, rechazada
    fecha_creada = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Cita {self.cita_id} - {self.fecha} {self.hora}>'
