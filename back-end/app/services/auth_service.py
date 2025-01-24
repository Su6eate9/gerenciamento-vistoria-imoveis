from flask import jsonify
from flask_mail import Message
from extensions import mail
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import Funcionario  # Substitua pelo nome correto do modelo
from database import db
import os

# Chave secreta obtida das variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")  # Substituir para produção


class AuthService:
    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username e senha são obrigatórios."}), 400

        # Busca o usuário no banco de dados
        user = Funcionario.query.filter_by(email=username).first()
        if not user or not check_password_hash(user.senha, password):
            return jsonify({"error": "Credenciais inválidas."}), 401

        # Gerar JWT
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "Login bem-sucedido.", "token": token}), 200

    @staticmethod
    def recover_password(data):
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email é obrigatório."}), 400

        # Busca o usuário no banco de dados
        user = Funcionario.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Gerar o link de recuperação
        recovery_token = jwt.encode({
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        recovery_link = f"http://localhost:5000/recover-password/{recovery_token}"  # Ajuste o domínio para produção

        # Enviar o e-mail
        try:
            msg = Message(
                subject="Recuperação de Senha",
                sender=os.getenv("MAIL_DEFAULT_SENDER"),
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

        # Localizar o usuário no banco de dados
        user = Funcionario.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Redefinir a senha
        new_password = data.get("new_password")
        if not new_password or len(new_password) < 8:
            return jsonify({"error": "A senha deve ter pelo menos 8 caracteres."}), 400

        user.senha = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Senha redefinida com sucesso."}), 200
