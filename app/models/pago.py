from app import db
#     Representa un pago asociado a una cita médica.

class Pago(db.Model):
    __tablename__ = 'pagos'
    __table_args__ = {'schema': 'centro_medico'}

    pago_id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('centro_medico.citas.cita_id'), nullable=False)
    estado = db.Column(db.String, nullable=False)  # pendiente, completado, fallido
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creada = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Pago {self.pago_id} - {self.estado}>'
