from database import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "Imobiliaria" ou "Vistoriador"
    cnpj = db.Column(db.String(18), unique=True, nullable=True)  # Apenas para Imobiliaria
    creci = db.Column(db.String(7), unique=True, nullable=True)  # Apenas para Vistoriador


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "tipo": self.tipo,
            "creci": self.creci if self.tipo == "Vistoriador" else None,
            "cnpj": self.cnpj if self.tipo == "Imobiliaria" else None
        }



# Tabela de Imóveis
class Imovel(db.Model):
    __tablename__ = 'imoveis'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String, nullable=False)
    endereco = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Ativo')
    proprietario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    proprietario = db.relationship('Funcionario', backref='imoveis')

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "endereco": self.endereco,
            "tipo": self.tipo,
            "status": self.status,
            "proprietario_id": self.proprietario_id
        }

# Tabela de Vistorias
class Vistoria(db.Model):
    __tablename__ = 'vistorias'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    vistoriador_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "data": str(self.data),
            "horario": str(self.horario),
            "status": self.status,
            "vistoriador_id": self.vistoriador_id,
            "imovel_id": self.imovel_id
        }


# Tabela de Agendamentos
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(db.Integer, db.ForeignKey('vistorias.id'), nullable=False)
    data = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Agendado')

# Tabela de Relatórios
class Relatorio(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(db.Integer, db.ForeignKey('vistorias.id'), nullable=False)
    vistoriador_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    texto = db.Column(db.String, nullable=False)
    data_geracao = db.Column(db.String, nullable=False)

# Tabela de Fotos
class Foto(db.Model):
    __tablename__ = 'fotos'
    id = db.Column(db.Integer, primary_key=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorios.id'), nullable=False)
    dados = db.Column(db.LargeBinary, nullable=False)  # Conteúdo binário da imagem
    nome_arquivo = db.Column(db.String, nullable=False)

# Tabela de Notificações
class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    mensagem = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)  # Tipo da notificação
    referencia_id = db.Column(db.Integer)  # ID do objeto relacionado (ex.: id da vistoria ou agendamento)
    data_criacao = db.Column(db.String, default=db.func.now())
    lida = db.Column(db.Boolean, default=False)
