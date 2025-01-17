from flask import jsonify
from datetime import datetime
from utils.helpers import find_by_id
from services.notificacao_service import NotificacaoService

VISTORIAS_DB = []
RELATORIOS_DB = []

class VistoriadorService:
    @staticmethod
    def registrar_inspecao(id, data):
        # Lógica para registrar inspeção
        vistoria = find_by_id(VISTORIAS_DB, data.get("vistoria_id"))
        if not vistoria or vistoria.get("vistoriador_id") != id:
            return jsonify({"error": "Vistoria não encontrada ou não atribuída ao vistoriador."}), 404

        if not all(k in data for k in ("observacoes", "fotos")):
            return jsonify({"error": "Dados incompletos para registrar a inspeção."}), 400

        relatorio = {
            "id": len(RELATORIOS_DB) + 1,
            "vistoria_id": vistoria["id"],
            "vistoriador_id": id,
            "observacoes": data["observacoes"],
            "fotos": data["fotos"],
            "data_criacao": datetime.utcnow()
        }
        RELATORIOS_DB.append(relatorio)

        mensagem = f"O relatório para a vistoria {vistoria['id']} foi registrado pelo vistoriador {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=vistoria.get("proprietario_id"))

        return jsonify({"message": "Relatório registrado com sucesso.", "relatorio": relatorio}), 200
