from flask import jsonify
from flask_mail import Message
from extensions import mail
from werkzeug.security import generate_password_hash, check_password_hash
from models import Funcionario
from database import db
import jwt
import datetime
import re
import os

SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")  # Use uma chave forte para produção


class AuthService:
    @staticmethod
    def login(data):
        """
        Verifica o tipo de número fornecido (CRECI ou CNPJ) e realiza o login.
        """
        numero = data.get("numero")  # Número fornecido no login (CNPJ ou CRECI)
        senha = data.get("senha")

        if not numero or not senha:
            return jsonify({"error": "Número e senha são obrigatórios."}), 400

        # Detectar se o número é CNPJ ou CRECI
        if AuthService.is_cnpj(numero):
            user = Funcionario.query.filter_by(cnpj=numero).first()
        elif AuthService.is_creci(numero):
            user = Funcionario.query.filter_by(creci=numero).first()
        else:
            return jsonify({"error": "Número inválido. Deve ser um CNPJ ou CRECI válido."}), 400

        if not user or not check_password_hash(user.senha, senha):
            return jsonify({"error": "Credenciais inválidas."}), 401

        # Gerar JWT
        token = jwt.encode({
            "id": user.id,
            "tipo": user.tipo,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "Login bem-sucedido.", "token": token}), 200

    @staticmethod
    def recover_password(data):
        """
        Envia um e-mail com um link para recuperação de senha.
        """
        email = data.get("email")
        if not email:
            return jsonify({"error": "E-mail é obrigatório."}), 400

        user = Funcionario.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Gerar link de recuperação
        recovery_token = jwt.encode({
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        recovery_link = f"http://localhost:5000/recover-password/{recovery_token}"

        try:
            # Enviar e-mail
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
        """
        Decodifica o token de recuperação e redefine a senha do usuário.
        """
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado."}), 400
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 400

        user = Funcionario.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        new_password = data.get("new_password")
        if not new_password or len(new_password) < 8:
            return jsonify({"error": "A senha deve ter pelo menos 8 caracteres."}), 400

        user.senha = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Senha redefinida com sucesso."}), 200

    @staticmethod
    def is_cnpj(numero):
        """
        Verifica se o número fornecido é um CNPJ válido.
        """
        cnpj_pattern = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"  # Formato: 00.000.000/0000-00
        return re.match(cnpj_pattern, numero)

    @staticmethod
    def is_creci(numero):
        """
        Verifica se o número fornecido é um CRECI válido.
        """
        creci_pattern = r"^\d{4,7}$"  # Exemplo: 1234567 (4 a 7 dígitos)
        return re.match(creci_pattern, numero)