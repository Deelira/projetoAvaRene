from flask import Flask

from .config import Config
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa as extensões (db e login_manager) com a app criada
    db.init_app(app)
    login_manager.init_app(app)

    # Importa os models para o Flask-SQLAlchemy "enxergar" as tabelas
    from . import models  # noqa: F401

    # Registra os blueprints (controllers)
    from .blueprints import auth_bp, servico_bp, contratacao_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(servico_bp)
    app.register_blueprint(contratacao_bp)

    # ---------- user_loader: como o Flask-Login recupera o usuário ----------
    from .services.usuario_service import UsuarioService

    @login_manager.user_loader
    def load_user(user_id):
        """Recebe o id (string) do cookie e retorna o Usuario correspondente."""
        return UsuarioService().buscar_por_id(int(user_id))

    # Cria as tabelas se ainda não existirem.
    # Para o projeto de faculdade isso é ok. Em produção usaríamos migrations.
    with app.app_context():
        db.create_all()

    return app