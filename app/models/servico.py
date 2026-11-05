from ..extensions import db
from datetime import datetime

class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Chave Estrangeira: Liga o serviço ao usuário (prestador) que o criou
    prestador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    # Relacionamento: Permite acessar o objeto do prestador (ex: servico.prestador.nome)
    prestador = db.relationship("Usuario", backref="servicos")

    def __repr__(self):
        return f"<Servico {self.id} - {self.titulo}>"