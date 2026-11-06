# app/__init__.py (trecho ajustado)
from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from . import models  # noqa: F401
    from .blueprints import auth_bp, servico_bp, contratacao_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(servico_bp)
    app.register_blueprint(contratacao_bp)

    @app.context_processor
    def inject_usuario():
        from .services.usuario_service import UsuarioService
        return dict(usuario=UsuarioService().usuario_logado())

    with app.app_context():
        db.create_all()

    return app