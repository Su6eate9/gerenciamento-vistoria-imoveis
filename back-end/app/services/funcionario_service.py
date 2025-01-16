from flask import jsonify
from utils.helpers import find_by_id

class FuncionarioService:
    @staticmethod
    def create_funcionario(data):
        # Lógica para criar funcionário
        return jsonify({"message": "Funcionario criado com sucesso."}), 201

    @staticmethod
    def agendar_vistoria(id, data):
        # Lógica para agendar vistoria
        return jsonify({"message": "Vistoria agendada com sucesso."}), 200

    @staticmethod
    def reagendar_vistoria(id, data):
        # Lógica para reagendar vistoria
        return jsonify({"message": "Vistoria reagendada com sucesso."}), 200
