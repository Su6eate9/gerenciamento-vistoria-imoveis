from services.notificacao_service import NotificacaoService
from models import Funcionario, Agendamento  # Importa os modelos ORM
from database import db  # Para gerenciar as transações do banco de dados
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import jsonify
from models import Funcionario
from database import db

class FuncionarioService:
    @staticmethod
    def create_funcionario(data):
        # Validação de campos obrigatórios
        if not all(k in data for k in ("nome", "email", "senha", "tipo")):
            return jsonify({"error": "Dados incompletos para criar funcionário."}), 400

        if data["tipo"] == "Imobiliaria" and not data.get("cnpj"):
            return jsonify({"error": "CNPJ é obrigatório para Imobiliárias."}), 400
        if data["tipo"] == "Vistoriador" and not data.get("cpf"):
            return jsonify({"error": "CPF é obrigatório para Vistoriadores."}), 400

        # Criar o funcionário
        funcionario = Funcionario(
            nome=data["nome"],
            email=data["email"],
            telefone=data.get("telefone"),
            senha=generate_password_hash(data["senha"]),
            creci=data.get("creci"),
            tipo=data["tipo"],
            cnpj=data.get("cnpj"),
            cpf=data.get("cpf")
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
