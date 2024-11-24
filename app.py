from flask import Flask, redirect
from flask_migrate import Migrate
from flask_admin import Admin
from flasgger import Swagger 
from sqlalchemy import event
from config.config import Config
from models.models import db, Usuario, ContaPagamento, Transacao, MetodoPagamento, TransacaoMetodo, LogOperacao
from views.views import CustomModelView
from api.api import api

#App Starter
app = Flask("Trabalho de LBD - Sistema de Pagamentos")
app.config.from_object(Config)

#Swagger Starter
swagger = Swagger(app)

#Api Starter
api.init_app(app)

#Database Starter
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
    
#Admin Page Starter
adminPage = Admin(app, name='Admin Page', template_mode="bootstrap4")

#Admin Page Views
adminPage.add_view(CustomModelView(Usuario, db.session))
adminPage.add_view(CustomModelView(ContaPagamento, db.session))
adminPage.add_view(CustomModelView(Transacao, db.session))
adminPage.add_view(CustomModelView(MetodoPagamento, db.session))
adminPage.add_view(CustomModelView(TransacaoMetodo, db.session))
adminPage.add_view(CustomModelView(LogOperacao, db.session))

#Routes
@app.route("/")
def home():
    return redirect('/admin')

#Host
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
