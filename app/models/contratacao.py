from ..extensions import db
from datetime import datetime

class Contratacao(db.Model):
    __tablename__ = "contratacoes"

    id = db.Column(db.Integer, primary_key=True)
    data_contratacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pendente") # Ex: pendente, aceito, concluido

    # Quem está contratando (Cliente)
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    cliente = db.relationship("Usuario", foreign_keys=[cliente_id], backref="minhas_contratacoes")

    # Qual serviço está sendo contratado
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=False)
    servico = db.relationship("Servico", backref="contratacoes_recebidas")

    def __repr__(self):
        return f"<Contratacao {self.id} - Servico: {self.servico_id} por Cliente: {self.cliente_id}>"