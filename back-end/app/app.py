from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()
# Inicializar o Flask
app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Inicializar o Flask-Mail
mail = Mail(app)

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

if __name__ == '__main__':
    app.run(debug=True)
