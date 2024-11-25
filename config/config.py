import os

"""
    Ao subir o container via compose, as variáveis do postgres serão reconhecidas pelo arquivo `.env`
"""
class Config:
    
    
    # >>> ORM <<<
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')
    SECRET_KEY = os.getenv('SECRET_KEY','ChavesChavesChaves')

    @staticmethod
    def get_database_uri():
        
        #Usuario da Database
        DB_USER = os.getenv('DB_USER','postgres')
        #Senha do usuario da DB
        DB_PASSWORD = os.getenv('DB_PASSWORD','postgres')    
        #Endereco do Servidor DB
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        #Porta de Conexao ao DB
        DB_PORT = os.getenv('DB_PORT', '5432')
        #Tipo de database
        DB_NAME = os.getenv('DB_NAME', 'postgres')
        
        DB_TYPE = os.getenv('DB_TYPE','postgres')
        
        if DB_TYPE == "mysql":

            return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        elif DB_TYPE == "postgres":

            return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_DATABASE_URI = get_database_uri()
        