from app import db

class Pago(db.Model):
    __tablename__ = 'pagos'
    __table_args__ = {'schema': 'centro_medico'}

    pago_id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('centro_medico.citas.cita_id'), nullable=False)
    estado = db.Column(db.String(20), nullable=False)  # pendiente, completado, fallido
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creada = db.Column(db.DateTime, server_default=db.func.now())
    id_pago_stripe = db.Column(db.String(100), index=True)
    metodo_pago = db.Column(db.String(50))

    # Relación con Cita (usando backref en lugar de back_populates)
    cita = db.relationship('Cita', backref='pagos')

    def __repr__(self):
        return f'<Pago {self.pago_id} - {self.estado}>'