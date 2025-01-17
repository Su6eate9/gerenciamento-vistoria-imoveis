from flask import jsonify
from utils.helpers import find_by_id
from services.notificacao_service import NotificacaoService
from datetime import datetime

FUNCIONARIOS_DB = []
AGENDAMENTOS_DB = []

class FuncionarioService:
    @staticmethod
    def create_funcionario(data):
        # Lógica para criar funcionário
        if not all(k in data for k in ("id", "email", "telefone", "senha", "creci")):
            return jsonify({"error": "Dados incompletos para criar o funcionário."}), 400

        if any(f["id"] == data["id"] for f in FUNCIONARIOS_DB):
            return jsonify({"error": "Funcionário com este ID já existe."}), 400

        funcionario = {
            "id": data["id"],
            "email": data["email"],
            "telefone": data["telefone"],
            "senha": data["senha"],
            "creci": data["creci"]
        }
        FUNCIONARIOS_DB.append(funcionario)
        return jsonify({"message": "Funcionario criado com sucesso.", "funcionario": funcionario}), 201

    @staticmethod
    def agendar_vistoria(id, data):
        # Lógica para agendar vistoria
        funcionario = find_by_id(FUNCIONARIOS_DB, id)
        if not funcionario:
            return jsonify({"error": "Funcionário não encontrado."}), 404

        if not all(k in data for k in ("id", "vistoria_id", "data", "horario")):
            return jsonify({"error": "Dados incompletos para agendar vistoria."}), 400

        agendamento = {
            "id": data["id"],
            "vistoria_id": data["vistoria_id"],
            "data": data["data"],
            "horario": data["horario"],
            "funcionario_id": id
        }
        AGENDAMENTOS_DB.append(agendamento)

        mensagem = f"Vistoria agendada para {data['data']} às {data['horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria agendada com sucesso.", "agendamento": agendamento}), 200

    @staticmethod
    def reagendar_vistoria(id, data):
        # Lógica para reagendar vistoria
        agendamento = find_by_id(AGENDAMENTOS_DB, data.get("agendamento_id"))
        if not agendamento or agendamento["funcionario_id"] != id:
            return jsonify({"error": "Agendamento não encontrado ou não pertence ao funcionário."}), 404

        if not all(k in data for k in ("nova_data", "novo_horario")):
            return jsonify({"error": "Dados incompletos para reagendar vistoria."}), 400

        agendamento["data"] = data["nova_data"]
        agendamento["horario"] = data["novo_horario"]

        mensagem = f"Vistoria reagendada para {data['nova_data']} às {data['novo_horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria reagendada com sucesso.", "agendamento": agendamento}), 200
