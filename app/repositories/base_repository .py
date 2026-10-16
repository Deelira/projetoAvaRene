from ..extensions import db

class BaseRepository:

    def __init__(self, model):
        self.model = model

    def criar(self, model):
        obj = self.model(model)
        db.session.add(obj)
        db.session.commit()
        return obj

    def buscar_por_id(self, id):
        return self.model.query.get(id)

    def listar(self):
        return self.model.query.all()

    def atualizar(self, obj, model):
        for k, n in model.items():
            setattr(obj, k, n)
        db.session.commit()
        return obj

    def deletar(self, obj):
        db.session.delete(obj)
        db.session.commit()
        