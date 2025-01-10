class Funcionario:
    def __init__(self, id, email, telefone, senha, creci):
        self.id = id
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.creci = creci
        self.notificacoes = []
        self.agendamentos = []

    def agendar_vistoria(self, agendamento):
        self.agendamentos.append(agendamento)
        print(f"Vistoria agendada para {agendamento.data} às {agendamento.horario}.")

    def reagendar_vistoria(self, agendamento_id, nova_data, novo_horario):
        for agendamento in self.agendamentos:
            if agendamento.id == agendamento_id:
                agendamento.data = nova_data
                agendamento.horario = novo_horario
                print(f"Vistoria {agendamento_id} reagendada para {nova_data} às {novo_horario}.")
                return
        print(f"Agendamento {agendamento_id} não encontrado.")

    def cadastrar_imovel(self, imovel):
        print(f"Imóvel cadastrado: {imovel.descricao} - {imovel.endereco.cep}")

    def editar_imovel(self, imovel_id, novos_dados):
        # Aqui implementa-se a lógica para editar os atributos do imóvel.
        print(f"Imóvel {imovel_id} atualizado com os novos dados: {novos_dados}")


class Imobiliaria(Funcionario):
    def __init__(self, id, email, telefone, senha, creci, cnpj, cep):
        super().__init__(id, email, telefone, senha, creci)
        self.cnpj = cnpj
        self.cep = cep

    def desativar_imovel(self, imovel_id):
        print(f"Imóvel {imovel_id} desativado.")

    def ativar_imovel(self, imovel_id):
        print(f"Imóvel {imovel_id} ativado.")

    def cancelar_vistoria(self, vistoria_id):
        print(f"Vistoria {vistoria_id} cancelada.")


class Vistoriador(Funcionario):
    def __init__(self, id, email, telefone, senha, creci, cpf):
        super().__init__(id, email, telefone, senha, creci)
        self.cpf = cpf
        self.vistorias = []
        self.relatorios = []

    def registrar_inspecao(self, vistoria_id, relatorio):
        self.relatorios.append(relatorio)
        print(f"Relatório registrado para vistoria {vistoria_id}.")


class Agendamento:
    def __init__(self, id, vistoria_id, data, horario):
        self.id = id
        self.vistoria_id = vistoria_id
        self.data = data
        self.horario = horario


class Vistoria:
    def __init__(self, id, vistoriador_id, imovel_id, data, horario, status, relatorio, imovel):
        self.id = id
        self.vistoriador_id = vistoriador_id
        self.imovel_id = imovel_id
        self.data = data
        self.horario = horario
        self.status = status
        self.relatorio = relatorio
        self.imovel = imovel


class Imovel:
    def __init__(self, id, proprietario_id, descricao, tipo, endereco):
        self.id = id
        self.proprietario_id = proprietario_id
        self.descricao = descricao
        self.tipo = tipo
        self.endereco = endereco


class Relatorio:
    def __init__(self, id, vistoria_id, vistoriador_id, textos, fotos):
        self.id = id
        self.vistoria_id = vistoria_id
        self.vistoriador_id = vistoriador_id
        self.textos = textos
        self.fotos = fotos



