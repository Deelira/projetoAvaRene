from ..extensions import db


class BaseRepository:
    """Repositório genérico com operações básicas de CRUD.

    Recebe um model (classe) no construtor e reutiliza os métodos para
    qualquer tabela. Repositórios específicos herdam desta classe.
    """

    def __init__(self, model):
        self.model = model

    # ---------- CREATE ----------
    def criar(self, **kwargs):
        """Cria um novo registro a partir dos campos passados como kwargs."""
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    # ---------- READ ----------
    def buscar_por_id(self, id):
        """Busca um registro pelo id. Retorna None se não existir."""
        return db.session.get(self.model, id)

    def listar(self):
        """Retorna todos os registros da tabela."""
        return self.model.query.all()

    def buscar_por_campo(self, campo: str, valor):
        """Retorna o primeiro registro onde `campo == valor` (ou None).

        Exemplo: repo.buscar_por_campo("email", "a@b.com")
        """
        return self.model.query.filter_by(**{campo: valor}).first()

    def listar_por_campo(self, campo: str, valor):
        """Retorna todos os registros onde `campo == valor`."""
        return self.model.query.filter_by(**{campo: valor}).all()

    # ---------- UPDATE ----------
    def atualizar(self, obj, dados: dict):
        """Atualiza os campos de `obj` com os pares chave/valor de `dados`."""
        for campo, valor in dados.items():
            setattr(obj, campo, valor)
        db.session.commit()
        return obj

    # ---------- DELETE ----------
    def deletar(self, obj):
        """Remove o registro do banco."""
        db.session.delete(obj)
        db.session.commit()