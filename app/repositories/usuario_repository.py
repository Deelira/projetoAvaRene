from .base_repository import BaseRepository
from ..models.usuario import Usuario


class UsuarioRepository(BaseRepository):
    """Repositório específico de Usuario.

    Herda todos os métodos CRUD do BaseRepository e adiciona
    consultas específicas do domínio de usuário.
    """

    def __init__(self):
        super().__init__(Usuario)

    def buscar_por_email(self, email: str):
        """Retorna o usuário com o email informado, ou None."""
        return self.buscar_por_campo("email", email)

    def listar_por_tipo(self, tipo):
        """Retorna todos os usuários de um determinado tipo (TipoUsuario)."""
        return self.listar_por_campo("tipo", tipo)