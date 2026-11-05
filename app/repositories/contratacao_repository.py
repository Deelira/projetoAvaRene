from .base_repository import BaseRepository
from ..models.contratacao import Contratacao
from ..models.servico import Servico

class ContratacaoRepository(BaseRepository):
    """Repositório de Contratações."""

    def __init__(self):
        super().__init__(Contratacao)

    def listar_por_cliente(self, cliente_id: int):
        """Retorna os pedidos feitos por um cliente específico."""
        return self.listar_por_campo("cliente_id", cliente_id)

    def listar_por_prestador(self, prestador_id: int):
        """Retorna os pedidos recebidos por um prestador.
        
        Como a Contratacao não tem o ID do prestador (só do serviço), 
        precisamos fazer um JOIN com a tabela de Servicos.
        """
        return Contratacao.query.join(Servico).filter(Servico.prestador_id == prestador_id).all()