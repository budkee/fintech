from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, text, func
from sqlalchemy.event import listens_for

db = SQLAlchemy()

# Define the Usuario model
class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    usuario_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    
    conta_pagamento = db.relationship("ContaPagamento", back_populates="usuario", uselist=False)
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

# Define the ContaPagamento model
class ContaPagamento(db.Model):
    __tablename__ = 'conta_pagamento'
    
    conta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), unique=True)
    saldo = db.Column(db.Numeric(10, 2))
    
    usuario = db.relationship("Usuario", back_populates="conta_pagamento")
    transacoes_origem = db.relationship("Transacao", foreign_keys="Transacao.conta_origem", back_populates="conta_origem_ref")
    transacoes_destino = db.relationship("Transacao", foreign_keys="Transacao.conta_destino", back_populates="conta_destino_ref")
    
    def __repr__(self):
        return f"<ContaPagamento {self.conta_id}>"

# Define the Transacao model
class Transacao(db.Model):
    __tablename__ = 'transacao'
    
    transacao_id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Numeric(10, 2))
    tipo = db.Column(db.String(50))
    status = db.Column(db.String(50))
    conta_origem = db.Column(db.Integer, db.ForeignKey('conta_pagamento.conta_id'))
    conta_destino = db.Column(db.Integer, db.ForeignKey('conta_pagamento.conta_id'))
    
    conta_origem_ref = db.relationship("ContaPagamento", foreign_keys=[conta_origem], back_populates="transacoes_origem")
    conta_destino_ref = db.relationship("ContaPagamento", foreign_keys=[conta_destino], back_populates="transacoes_destino")
    metodos_pagamento = db.relationship("TransacaoMetodo", back_populates="transacao")
    
    def __repr__(self):
        return f"<Transacao {self.transacao_id}>"

# Define the MetodoPagamento model
class MetodoPagamento(db.Model):
    __tablename__ = 'metodo_pagamento'
    
    metodo_id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    
    transacoes = db.relationship("TransacaoMetodo", back_populates="metodo_pagamento")
    
    def __repr__(self):
        return f"<MetodoPagamento {self.descricao}>"

class TransacaoMetodo(db.Model):
    __tablename__ = 'transacao_metodo'
    
    transacao_id = db.Column(db.Integer, db.ForeignKey('transacao.transacao_id'), primary_key=True)
    metodo_id = db.Column(db.Integer, db.ForeignKey('metodo_pagamento.metodo_id'), primary_key=True)
    
    # Relacionamentos com back_populates
    transacao = db.relationship("Transacao", back_populates="metodos_pagamento")
    metodo_pagamento = db.relationship("MetodoPagamento", back_populates="transacoes")
    
    def __repr__(self):
        return f"<TransacaoMetodo transacao_id={self.transacao_id} metodo_id={self.metodo_id}>"
    
class LogOperacao(db.Model):
    __tablename__ = 'log_operacao'
    
    log_id = db.Column(db.Integer, primary_key=True)
    tabela = db.Column(db.String(255), nullable=False)  
    operacao = db.Column(db.String(50), nullable=False)
    data_operacao = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp()) # Valor padrão
    registro_antigo = db.Column(db.Text)  
    registro_novo = db.Column(db.Text)



def create_triggers_for_table(table_name, columns, connection, database_url):
    """Função para criar triggers para uma tabela específica, verificando se já existem."""
    column_names = ', '.join([f"'{col}', NEW.{col}" for col in columns])
    column_names_old = ', '.join([f"'{col}', OLD.{col}" for col in columns])

    def trigger_exists(trigger_name):
        """Verifica se o trigger já existe no banco de dados."""
        if "mysql" in database_url:
            query = text("""
                SELECT COUNT(*)
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE() AND TRIGGER_NAME = :trigger_name
            """)
        elif "postgresql" in database_url:
            query = text("""
                SELECT COUNT(*)
                FROM pg_trigger
                WHERE tgname = :trigger_name
            """)
        else:
            raise ValueError(f"Banco de dados {database_url} não suportado para verificação de triggers.")
        
        result = connection.execute(query, {"trigger_name": trigger_name}).scalar()
        return result > 0

    # Criação condicional para cada trigger no MySQL
    if "mysql" in database_url:
        if not trigger_exists(f"{table_name}_log_insert"):
            trigger_insert = f"""
            CREATE TRIGGER {table_name}_log_insert
            AFTER INSERT ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO log_operacao (tabela, operacao, registro_novo)
                VALUES ('{table_name}', 'INSERT', JSON_OBJECT({column_names}));
            END;
            """
            connection.execute(text(trigger_insert))

        if not trigger_exists(f"{table_name}_log_update"):
            trigger_update = f"""
            CREATE TRIGGER {table_name}_log_update
            AFTER UPDATE ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO log_operacao (tabela, operacao, registro_antigo, registro_novo)
                VALUES ('{table_name}', 'UPDATE', 
                        JSON_OBJECT({column_names_old}),
                        JSON_OBJECT({column_names}));
            END;
            """
            connection.execute(text(trigger_update))

        if not trigger_exists(f"{table_name}_log_delete"):
            trigger_delete = f"""
            CREATE TRIGGER {table_name}_log_delete
            AFTER DELETE ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO log_operacao (tabela, operacao, registro_antigo)
                VALUES ('{table_name}', 'DELETE', JSON_OBJECT({column_names_old}));
            END;
            """
            connection.execute(text(trigger_delete))
    
    elif "postgresql" in database_url:
        # PostgreSQL Trigger Function
        if not trigger_exists(f"{table_name}_log"):
            trigger_function = f"""
            CREATE OR REPLACE FUNCTION log_{table_name}_operations()
            RETURNS TRIGGER AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO log_operacao (tabela, operacao, registro_novo)
                    VALUES ('{table_name}', TG_OP, row_to_json(NEW)::text);
                ELSIF TG_OP = 'UPDATE' THEN
                    INSERT INTO log_operacao (tabela, operacao, registro_antigo, registro_novo)
                    VALUES ('{table_name}', TG_OP, row_to_json(OLD)::text, row_to_json(NEW)::text);
                ELSIF TG_OP = 'DELETE' THEN
                    INSERT INTO log_operacao (tabela, operacao, registro_antigo)
                    VALUES ('{table_name}', TG_OP, row_to_json(OLD)::text);
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
            """
            trigger_sql = f"""
            CREATE TRIGGER {table_name}_log
            AFTER INSERT OR UPDATE OR DELETE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION log_{table_name}_operations();
            """
            connection.execute(text(trigger_function))
            connection.execute(text(trigger_sql))
    
@listens_for(db.Model.metadata, 'after_create')
def create_triggers_for_all_tables(target, connection, **kw):
    database_url = connection.engine.url.drivername
    
    # Itera sobre todas as tabelas do metadata
    for table_name, table in target.tables.items():
        if table_name != "log_operacao":  # Ignora a tabela de log
            columns = [col.name for col in table.columns]
            create_triggers_for_table(table_name, columns, connection, database_url)
