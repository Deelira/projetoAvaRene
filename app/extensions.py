from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Objeto do banco de dados (SQLAlchemy).
# Criado sem app ainda; será inicializado no app/__init__.py.
db = SQLAlchemy()

# Gerenciador de sessões de login do Flask-Login.
# Também criado sem app; será inicializado no app/__init__.py.
login_manager = LoginManager()

# Para onde o Flask-Login redireciona quando alguém tenta acessar
# uma rota protegida (@login_required) sem estar logado.
login_manager.login_view = "auth.login"

# Mensagem exibida quando o usuário é redirecionado (usada com flash()).
login_manager.login_message = "Você precisa estar logado para acessar esta página."
login_manager.login_message_category = "warning"