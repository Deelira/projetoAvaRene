import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://conecta:senha123@localhost:5432/conectaserv"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    