from flask import jsonify
from datetime import datetime

NOTIFICACOES_DB = []

class NotificacaoService:
    @staticmethod
    def criar_notificacao(mensagem, destinatario_id):
        nova_notificacao = {
            "id": len(NOTIFICACOES_DB) + 1,
            "mensagem": mensagem,
            "destinatario_id": destinatario_id,
            "data_criacao": datetime.utcnow(),
            "status": "não lida"
        }
        NOTIFICACOES_DB.append(nova_notificacao)
        return nova_notificacao

    @staticmethod
    def listar_notificacoes(destinatario_id):
        notificacoes = [n for n in NOTIFICACOES_DB if n["destinatario_id"] == destinatario_id]
        return jsonify(notificacoes), 200

    @staticmethod
    def marcar_como_lida(id):
        for notificacao in NOTIFICACOES_DB:
            if notificacao["id"] == id:
                notificacao["status"] = "lida"
                return jsonify({"message": "Notificação marcada como lida."}), 200
        return jsonify({"error": "Notificação não encontrada."}), 404
