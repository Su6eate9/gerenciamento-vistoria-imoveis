from flask import jsonify
from utils.helpers import find_by_id
from services.notificacao_service import NotificacaoService
from models import Funcionario, Agendamento  # Importa os modelos ORM
from database import db  # Para gerenciar as transações do banco de dados
from datetime import datetime
from werkzeug.security import generate_password_hash

class FuncionarioService:
    @staticmethod
    def create_funcionario(data):
        # Validação de dados
        if not all(k in data for k in ("email", "telefone", "senha", "creci", "nome", "tipo")):
            return jsonify({"error": "Dados incompletos para criar o funcionário."}), 400

        # Verifica se o e-mail já está em uso
        if Funcionario.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "E-mail já registrado."}), 400

        # Criação do funcionário
        funcionario = Funcionario(
            nome=data["nome"],
            email=data["email"],
            telefone=data["telefone"],
            senha=generate_password_hash(data["senha"]),
            creci=data["creci"],
            tipo=data["tipo"],
            cpf=data.get("cpf"),
            cnpj=data.get("cnpj")
        )

        db.session.add(funcionario)
        db.session.commit()

        return jsonify({"message": "Funcionário criado com sucesso.", "funcionario": funcionario.to_dict()}), 201

    @staticmethod
    def agendar_vistoria(id, data):
        # Busca o funcionário
        funcionario = Funcionario.query.get(id)
        if not funcionario:
            return jsonify({"error": "Funcionário não encontrado."}), 404

        # Validação de dados do agendamento
        if not all(k in data for k in ("vistoria_id", "data", "horario")):
            return jsonify({"error": "Dados incompletos para agendar vistoria."}), 400

        # Criação do agendamento
        agendamento = Agendamento(
            vistoria_id=data["vistoria_id"],
            data=data["data"],
            horario=data["horario"],
            funcionario_id=id
        )

        db.session.add(agendamento)
        db.session.commit()

        # Notificação
        mensagem = f"Vistoria agendada para {data['data']} às {data['horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria agendada com sucesso.", "agendamento": agendamento.to_dict()}), 200

    @staticmethod
    def reagendar_vistoria(id, data):
        # Busca o agendamento
        agendamento = Agendamento.query.filter_by(id=data.get("agendamento_id"), funcionario_id=id).first()
        if not agendamento:
            return jsonify({"error": "Agendamento não encontrado ou não pertence ao funcionário."}), 404

        # Validação de dados do reagendamento
        if not all(k in data for k in ("nova_data", "novo_horario")):
            return jsonify({"error": "Dados incompletos para reagendar vistoria."}), 400

        # Atualização do agendamento
        agendamento.data = data["nova_data"]
        agendamento.horario = data["novo_horario"]
        db.session.commit()

        # Notificação
        mensagem = f"Vistoria reagendada para {data['nova_data']} às {data['novo_horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria reagendada com sucesso.", "agendamento": agendamento.to_dict()}), 200
