from ..models.usuario import Usuario, TipoUsuario
from ..repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    """Regras de negócio relacionadas a usuários.

    O service NÃO acessa o banco diretamente: sempre usa o repositório.
    O controller (Blueprint) NÃO contém regras: sempre usa o service.
    """

    def __init__(self):
        self.repo = UsuarioRepository()

    # ---------- CREATE ----------
    def criar_usuario(self, nome: str, email: str, senha: str, tipo: TipoUsuario = TipoUsuario.CLIENTE) -> Usuario:
        """Valida, hasheia a senha e salva um novo usuário.

        Lança ValueError quando os dados são inválidos.
        """
        # 1. Validação básica
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        if not email or "@" not in email:
            raise ValueError("Informe um e-mail válido.")
        if not senha or len(senha) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")

        # 2. Normaliza o e-mail (minúsculo, sem espaços)
        email = email.strip().lower()

        # 3. Regra de negócio: e-mail único
        if self.repo.buscar_por_email(email):
            raise ValueError("Já existe um usuário cadastrado com esse e-mail.")

        # 4. Monta o objeto (NÃO chamamos o repo.criar direto, porque
        #    precisamos hashear a senha ANTES de salvar).
        usuario = Usuario(nome=nome.strip(), email=email, tipo=tipo)
        usuario.set_senha(senha)

        # 5. Persiste
        return self.repo.criar(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=usuario.senha_hash,
            tipo=usuario.tipo,
        )

    # ---------- READ ----------
    def buscar_por_id(self, id: int):
        """Usado pelo Flask-Login (user_loader) para recuperar o usuário."""
        return self.repo.buscar_por_id(id)

    def buscar_por_email(self, email: str):
        """Retorna o usuário com o e-mail informado, ou None."""
        return self.repo.buscar_por_email(email.strip().lower())

    def listar_usuarios(self):
        """Retorna todos os usuários cadastrados."""
        return self.repo.listar()

    # ---------- AUTH ----------
    def autenticar(self, email: str, senha: str):
        """Verifica e-mail + senha. Retorna o Usuario se ok, ou None."""
        if not email or not senha:
            return None

        usuario = self.repo.buscar_por_email(email.strip().lower())
        if not usuario:
            return None

        if not usuario.checar_senha(senha):
            return None

        return usuario

      # ---------- UPDATE ----------
    def tornar_prestador(self, usuario_id: int):
        """Muda o tipo do usuário de CLIENTE para PRESTADOR."""
        usuario = self.repo.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario.tipo == TipoUsuario.PRESTADOR:
            raise ValueError("Você já é um prestador.")

        # Muda o tipo e salva
        self.repo.atualizar(usuario, {"tipo": TipoUsuario.PRESTADOR})
        return usuario