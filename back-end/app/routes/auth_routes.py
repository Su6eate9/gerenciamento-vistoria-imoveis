from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Credenciais incompletas."}), 400
        return AuthService.login(data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@auth_bp.route('/auth/recover', methods=['POST'])
def recover_password():
    try:
        data = request.json
        if not data or "email" not in data:
            return jsonify({"error": "E-mail é obrigatório."}), 400
        return AuthService.recover_password(data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@auth_bp.route('/recover-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        data = request.json
        if not data or "new_password" not in data:
            return jsonify({"error": "Nova senha é obrigatória."}), 400
        return AuthService.reset_password(token, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
