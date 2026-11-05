from ..repositories.contratacao_repository import ContratacaoRepository
from ..repositories.servico_repository import ServicoRepository
from ..models.usuario import TipoUsuario


class ContratacaoService:
    """Regras de negócio relacionadas a Contratações."""

    def __init__(self):
        self.repo = ContratacaoRepository()
        self.servico_repo = ServicoRepository()

    # ---------- CREATE ----------
    def contratar_servico(self, usuario_logado, servico_id: int):
        """Valida e cria uma nova contratação."""
        
        # Regra 1: Apenas clientes podem contratar
        if usuario_logado.tipo not in [TipoUsuario.CLIENTE, TipoUsuario.PRESTADOR]:
            raise ValueError("Apenas usuários logados podem contratar serviços.")

        # Regra 2: O serviço precisa existir no banco
        servico = self.servico_repo.buscar_por_id(servico_id)
        if not servico:
            raise ValueError("Serviço não encontrado.")

        # Regra 3: Impedir que o prestador contrate o próprio serviço 
        # (redundante por causa da Regra 1, mas é uma boa prática de segurança)
        if servico.prestador_id == usuario_logado.id:
            raise ValueError("Você não pode contratar o seu próprio serviço.")

        # Se passou por tudo, cria a contratação com status padrão "pendente"
        return self.repo.criar(
            cliente_id=usuario_logado.id,
            servico_id=servico.id
        )

    # ---------- READ ----------
    def listar_minhas_contratacoes(self, cliente_id: int):
        """Para o cliente ver o que ele contratou."""
        return self.repo.listar_por_cliente(cliente_id)

    def listar_pedidos_recebidos(self, prestador_id: int):
        """Para o prestador ver quem quer seus serviços."""
        return self.repo.listar_por_prestador(prestador_id)