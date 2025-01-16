from flask import jsonify

class ImobiliariaService:
    @staticmethod
    def desativar_imovel(id, data):
        # Lógica para desativar imóvel
        return jsonify({"message": "Imóvel desativado com sucesso."}), 200

    @staticmethod
    def ativar_imovel(id, data):
        # Lógica para ativar imóvel
        return jsonify({"message": "Imóvel ativado com sucesso."}), 200

    @staticmethod
    def cancelar_vistoria(id, data):
        # Lógica para cancelar vistoria
        return jsonify({"message": "Vistoria cancelada com sucesso."}), 200
