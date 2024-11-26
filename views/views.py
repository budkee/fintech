from flask_admin.contrib.sqla import ModelView
from models.models import db
from wtforms import StringField, IntegerField, DecimalField
from flask_admin.form import rules
from wtforms.validators import Optional

# Define a custom ModelView for Usuario

class CustomModelView(ModelView):
    column_display_pk = True
    can_export = True
    can_view_details = True

    def __init__(self, model, session, **kwargs):
        self.column_list = [column.key for column in model.__table__.columns]
        self.column_searchable_list = [column.key for column in model.__table__.columns]
        self.column_filters = [column.key for column in model.__table__.columns]
        self.column_sortable_list = [column.key for column in model.__table__.columns]
        
        self.form_create_rules = self._generate_form_create_rules(model)
        self.form_extra_fields = self._generate_form_extra_fields(model)
        super().__init__(model, session, **kwargs)
    
    def _generate_form_create_rules(self, model):
        fields = [column.key for column in model.__table__.columns]
        return (rules.FieldSet(fields, f"{model.__name__} Campos"),)

    def _generate_form_extra_fields(self, model):
        extra_fields = {}
        for column in model.__table__.columns:
            field_args = {}
            # Adiciona o valor padrão, se definido
            if column.default is not None:
                field_args['default'] = column.default.arg
            
            # Permite valores nulos
            field_args['validators'] = [Optional()]

            # Associa os campos de acordo com o tipo de dado
            if isinstance(column.type, db.Integer):
                extra_fields[column.key] = IntegerField(column.key.capitalize(), **field_args)
            elif isinstance(column.type, db.Numeric):
                extra_fields[column.key] = DecimalField(
                    column.key.capitalize(), places=2, **field_args
                )
            elif isinstance(column.type, (db.String, db.Text)):
                extra_fields[column.key] = StringField(column.key.capitalize(), **field_args)
        return extra_fields
