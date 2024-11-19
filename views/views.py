from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, IntegerField, DecimalField
from flask_admin.model.form import BaseForm
from flask_admin.form import rules

# Define a custom ModelView for Usuario
class UsuarioModelView(ModelView):
    column_list = ('usuario_id', 'nome', 'email', 'telefone', 'cpf')
    column_searchable_list = ('usuario_id', 'nome', 'email', 'telefone', 'cpf')
    column_filters = ('usuario_id', 'nome', 'email', 'telefone', 'cpf')
    column_sortable_list = ('usuario_id', 'nome', 'email', 'telefone', 'cpf')
    
    form_create_rules = (
        rules.FieldSet(('nome', 'email', 'telefone', 'cpf'), 'Usuario'),
    )

    can_export = True
    can_view_details = True

# Define a custom ModelView for ContaPagamento
class ContaPagamentoModelView(ModelView):
    
    column_list = ('conta_id', 'usuario_id', 'nome_usuario', 'saldo')
    column_searchable_list = ('conta_id', 'usuario_id', 'saldo')
    column_filters = ('conta_id', 'usuario_id', 'saldo')
    column_sortable_list = ('conta_id', 'usuario_id', 'saldo')
    
    # Form rules for the fields during creation
    form_create_rules = (
        rules.FieldSet(('usuario_id', 'saldo'), 'Conta Pagamento'),
    )
    
    # Custom column formatters to display the user name instead of the user ID
    column_formatters = {
        'nome_usuario': lambda v, c, m, p: m.usuario.nome if m.usuario else ''
    }
    
    can_export = True
    can_view_details = True
    
    # Adding fields to form_extra_fields for better customization and rendering
    form_extra_fields = {
        'usuario_id': IntegerField('Usuario Id'),
        'saldo': DecimalField('Saldo', places=2)
    }


# Define a custom ModelView for Transacao
class TransacaoModelView(ModelView):
    column_list = ('transacao_id', 'data', 'valor', 'tipo', 'status', 'conta_origem','conta_destino')
    column_searchable_list = ('transacao_id', 'data', 'valor', 'tipo', 'status','conta_origem','conta_destino')
    column_filters = ('transacao_id','data', 'tipo', 'status','conta_origem','conta_destino')
    column_sortable_list = ('transacao_id', 'data', 'valor', 'tipo', 'status','conta_origem','conta_destino')
    
    form_create_rules = (
        rules.FieldSet(('data', 'valor', 'tipo', 'status','conta_origem','conta_destino'),'Transacao'),
    )
    
    form_extra_fields = {
        'conta_origem': IntegerField('Conta Origem'),
        'conta_destino': DecimalField('Conta Destino', places=2)
    }
    
    can_export = True
    can_view_details = True

    # Exibir os dados da conta de origem e destino
    column_formatters = {
        'conta_origem': lambda v, c, m, p: m.conta_origem_ref.conta_id if m.conta_origem_ref else '',
        'conta_destino': lambda v, c, m, p: m.conta_destino_ref.conta_id if m.conta_destino_ref else ''
    }

# Define a custom ModelView for MetodoPagamento
class MetodoPagamentoModelView(ModelView):
    column_list = ('metodo_id', 'descricao')
    column_searchable_list = ('metodo_id', 'descricao')
    column_filters = ('metodo_id', 'descricao')
    column_sortable_list = ('metodo_id', 'descricao')

    form_create_rules = (
        rules.FieldSet(('descricao',),'Metodo Pagamento'),
    )

    can_export = True
    can_view_details = True
    
class Transacao_MetodoModelView(ModelView):
    column_list = ('transacao_id','metodo_id','descricao')
    column_searchable_list = ('transacao_id','metodo_id')
    column_filters = ('transacao_id','metodo_id')
    column_sortable_list = ('transacao_id','metodo_id')
    
    form_create_rules = (
        rules.FieldSet(('transacao_id','metodo_id'),'Transacao_Metodo'),
    )
    
    form_extra_fields = {
        'transacao_id': IntegerField('Transacao Id'),
        'metodo_id': IntegerField('Metodo Id')
    }
    
    can_export = True
    can_view_details = True
    
    column_formatters = {
        'descricao': lambda v, c, m, p: m.metodo_pagamento.descricao if m.metodo_pagamento else ''
    }