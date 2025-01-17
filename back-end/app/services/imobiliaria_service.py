from flask import jsonify
from utils.helpers import find_by_id
from services.notificacao_service import NotificacaoService

IMOVEIS_DB = []
VISTORIAS_DB = []

class ImobiliariaService:
    @staticmethod
    def desativar_imovel(id, data):
        # Lógica para desativar imóvel
        imovel = find_by_id(IMOVEIS_DB, data.get("imovel_id"))
        if not imovel:
            return jsonify({"error": "Imóvel não encontrado."}), 404

        imovel["status"] = "desativado"

        mensagem = f"O imóvel {imovel['id']} foi desativado pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=imovel.get("proprietario_id"))

        return jsonify({"message": "Imóvel desativado com sucesso.", "imovel": imovel}), 200

    @staticmethod
    def ativar_imovel(id, data):
        # Lógica para ativar imóvel
        imovel = find_by_id(IMOVEIS_DB, data.get("imovel_id"))
        if not imovel:
            return jsonify({"error": "Imóvel não encontrado."}), 404

        imovel["status"] = "ativo"

        mensagem = f"O imóvel {imovel['id']} foi ativado pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=imovel.get("proprietario_id"))

        return jsonify({"message": "Imóvel ativado com sucesso.", "imovel": imovel}), 200

    @staticmethod
    def cancelar_vistoria(id, data):
        # Lógica para cancelar vistoria
        vistoria = find_by_id(VISTORIAS_DB, data.get("vistoria_id"))
        if not vistoria:
            return jsonify({"error": "Vistoria não encontrada."}), 404

        VISTORIAS_DB.remove(vistoria)

        mensagem = f"A vistoria {vistoria['id']} foi cancelada pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=vistoria.get("vistoriador_id"))

        return jsonify({"message": "Vistoria cancelada com sucesso."}), 200
