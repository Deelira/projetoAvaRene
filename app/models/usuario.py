from ..extensions import db
from enum import Enum

class TipoUsuario(Enum):
    Cliente: "cliente"
    Prestador: "prestador"
    Admin: "admin"

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum(TipoUsuario, name="tipo_usuario"), nullable=False)
