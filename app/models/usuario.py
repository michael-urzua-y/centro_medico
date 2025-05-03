from app import db
#     Representa a un usuario del sistema, que puede ser un paciente o un médico.

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'centro_medico'}

    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    rol = db.Column(db.String, nullable=False)
    token = db.Column(db.String)

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.rol})>'
