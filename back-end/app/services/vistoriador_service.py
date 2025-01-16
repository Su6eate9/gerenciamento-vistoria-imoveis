from flask import jsonify

class VistoriadorService:
    @staticmethod
    def registrar_inspecao(id, data):
        # Lógica para registrar inspeção
        return jsonify({"message": "Relatório registrado com sucesso."}), 200
