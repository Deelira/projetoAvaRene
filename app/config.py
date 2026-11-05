import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se existir)
load_dotenv()


class Config:
    # Chave usada pelo Flask para assinar cookies de sessão (login, flash, etc).
    # Em produção, DEVE vir do ambiente. O fallback só serve para desenvolvimento.
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-chave-insegura-troque-em-producao")

    # String de conexão com o PostgreSQL, lida do .env.
    # Formato: postgresql+psycopg2://usuario:senha@host:porta/banco
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://conecta:senha123@localhost:5432/conectaserv",
    )

    # Evita o warning "SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead"
    SQLALCHEMY_TRACK_MODIFICATIONS = False