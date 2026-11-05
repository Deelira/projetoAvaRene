from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..extensions import db


class TipoUsuario(Enum):
    CLIENTE = "cliente"
    PRESTADOR = "prestador"
    ADMIN = "admin"


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(
        db.Enum(TipoUsuario, name="tipo_usuario"),
        nullable=False,
        default=TipoUsuario.CLIENTE,
    )

    # ---------- Senha ----------
    def set_senha(self, senha_texto_puro: str) -> None:
        """Recebe a senha em texto puro e guarda APENAS o hash no atributo senha_hash."""
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def checar_senha(self, senha_texto_puro: str) -> bool:
        """Compara a senha digitada com o hash salvo. Retorna True/False."""
        return check_password_hash(self.senha_hash, senha_texto_puro)

    # ---------- Debug ----------
    def __repr__(self) -> str:
        return f"<Usuario {self.id} - {self.email}>"