from .base_repository import BaseRepository
from ..models.servico import Servico


class ServicoRepository(BaseRepository):
    """Repositório específico de Serviço."""

    def __init__(self):
        super().__init__(Servico)

    def listar_por_prestador(self, prestador_id: int):
        """Retorna todos os serviços criados por um prestador específico."""
        return self.listar_por_campo("prestador_id", prestador_id)

    def listar_todos(self):
        """Retorna todos os serviços disponíveis no sistema (para clientes verem)."""
        return self.listar()