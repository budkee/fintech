import os

class Config:
    
    SECRET_KEY = os.getenv('SECRET_KEY','ChavesChavesChaves voce me deixa louco')
    #Paleta de cores do Bootstrap Swatch
    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH','yeti')
    #Track Modifications SqlAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS','False')
    #Usuario da Database
    DB_USER = os.getenv('DB_USER','root')
    #Senha do usuario da DB
    DB_PASSWORD = os.getenv('DB_PASSWORD','')    
    #Endereco do Servidor DB
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    #Porta de Conexao ao DB
    DB_PORT = os.getenv('DB_PORT', '3306')
    #Tipo de database
    DB_NAME = os.getenv('DB_NAME', 'mydb')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"