from flask import jsonify
from flask_mail import Message
from app import mail
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Simulação de base de dados de usuários
#Conferir integração com o BD
USERS_DB = [
    {"id": 1, "username": "admin", "password": generate_password_hash("admin123"), "email": "admin@example.com"},
    {"id": 2, "username": "vistoriador1", "password": generate_password_hash("password123"), "email": "vistoriador@example.com"},
]

SECRET_KEY = "LaraCroftTomb69Sharpei"  # Substituir por uma chave secreta real

class AuthService:
    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")
        user = next((u for u in USERS_DB if u["username"] == username), None)

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Credenciais inválidas."}), 401

        # Gerar JWT
        token = jwt.encode({
            "id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "Login bem-sucedido.", "token": token}), 200


    @staticmethod
    def recover_password(data):
        email = data.get("email")
        user = next((u for u in USERS_DB if u["email"] == email), None)

        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Gerar o link de recuperação
        recovery_link = f"http://example.com/recover-password/{user['id']}"

        # Enviar o e-mail
        try:
            msg = Message(
                subject="Recuperação de Senha",
                sender="techvanguardsolutions.imoveis@gmail.com",
                recipients=[email],
                body=f"Olá, clique no link abaixo para recuperar sua senha:\n\n{recovery_link}"
            )
            mail.send(msg)
            return jsonify({"message": "E-mail de recuperação enviado com sucesso."}), 200
        except Exception as e:
            return jsonify({"error": f"Falha ao enviar e-mail: {str(e)}"}), 500
    
    @staticmethod
    def reset_password(token, data):
        try:
            # Decodificar o token JWT
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado."}), 400
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 400

        # Localizar o usuário
        user = next((u for u in USERS_DB if u["id"] == user_id), None)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Redefinir a senha
        new_password = data.get("new_password")
        user["password"] = generate_password_hash(new_password)
        return jsonify({"message": "Senha redefinida com sucesso."}), 200