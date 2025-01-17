from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
from database import db, init_db
from flask_swagger_ui import get_swaggerui_blueprint

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Flask
app = Flask(__name__)

# Configuração do banco de dados (SQLite para desenvolvimento, outro para produção)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    f"sqlite:///{os.path.join(basedir, 'prototipo1.db')}"  # Padrão para desenvolvimento
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Inicializar extensões
mail = Mail(app)

# Inicializar o banco de dados
init_db(app)

# Registrar Blueprints
from routes.funcionario_routes import funcionario_bp
from routes.imobiliaria_routes import imobiliaria_bp
from routes.vistoriador_routes import vistoriador_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

app.register_blueprint(funcionario_bp)
app.register_blueprint(imobiliaria_bp)
app.register_blueprint(vistoriador_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)


SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'  # Arquivo JSON com a definição da API
swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
