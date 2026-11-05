from ..repositories.servico_repository import ServicoRepository
from ..models.servico import Servico


class ServicoService:
    """Regras de negócio relacionadas a Serviços."""

    def __init__(self):
        self.repo = ServicoRepository()

    # ---------- CREATE ----------
    def criar_servico(self, prestador_id: int, titulo: str, descricao: str, preco: str) -> Servico:
        """Valida os dados e cria um novo serviço para o prestador."""
        
        # 1. Validações básicas (Regra de Negócio)
        if not titulo or not titulo.strip():
            raise ValueError("O título do serviço é obrigatório.")
        if not descricao or not descricao.strip():
            raise ValueError("A descrição do serviço é obrigatória.")
        
        # 2. Converte o preço para número (do formulário HTML vem como texto)
        try:
            preco_float = float(preco)
        except (ValueError, TypeError):
            raise ValueError("O preço deve ser um número válido.")
            
        if preco_float <= 0:
            raise ValueError("O preço deve ser maior que zero.")

        # 3. Salva no banco via repositório
        return self.repo.criar(
            prestador_id=prestador_id,
            titulo=titulo.strip(),
            descricao=descricao.strip(),
            preco=preco_float
        )

    # ---------- READ ----------
    def listar_servicos_do_prestador(self, prestador_id: int):
        """Retorna os serviços criados por um prestador específico."""
        return self.repo.listar_por_prestador(prestador_id)

    def listar_catalogo(self):
        """Retorna todos os serviços disponíveis no sistema."""
        return self.repo.listar_todos()

    def buscar_por_id(self, servico_id: int):
        """Busca um serviço específico (útil na hora de contratar)."""
        return self.repo.buscar_por_id(servico_id)