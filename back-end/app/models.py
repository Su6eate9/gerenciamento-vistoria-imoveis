from database import db

# Tabela de Funcionários
class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telefone = db.Column(db.String)
    senha = db.Column(db.String, nullable=False)
    creci = db.Column(db.String)
    tipo = db.Column(db.String, nullable=False)  # 'Imobiliaria' ou 'Vistoriador'
    cpf = db.Column(db.String)  # Apenas para vistoriadores
    cnpj = db.Column(db.String)  # Apenas para imobiliárias

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

# Tabela de Vistorias
class Vistoria(db.Model):
    __tablename__ = 'vistorias'
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    vistoriador_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    data = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Pendente')

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
