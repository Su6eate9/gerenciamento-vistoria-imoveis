import sqlite3

def criar_tabelas():
    # Conecta ou cria o banco de dados SQLite
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()

    # Ativar suporte a chaves estrangeiras
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Script SQL para criar as tabelas
    script_sql = '''
    -- Tabela de Funcionários
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT,
        senha TEXT NOT NULL,
        creci TEXT, 
        tipo TEXT NOT NULL, -- Tipo: 'Imobiliaria' ou 'Vistoriador'
        cpf TEXT, -- Apenas para vistoriadores
        cnpj TEXT -- Apenas para imobiliárias
    );

    -- Tabela de Imóveis
    CREATE TABLE IF NOT EXISTS imoveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        endereco TEXT NOT NULL,
        tipo TEXT NOT NULL, -- Tipo: 'Casa', 'Apartamento', 'Comercial', 'Terreno'
        status TEXT NOT NULL DEFAULT 'Ativo', -- Ativo ou Desativado
        proprietario_id INTEGER, -- Associado ao funcionário (imobiliária)
        FOREIGN KEY (proprietario_id) REFERENCES funcionarios (id)
    );

    -- Tabela de Vistorias
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imovel_id INTEGER NOT NULL,
        vistoriador_id INTEGER NOT NULL,
        data TEXT NOT NULL, -- Data e horário da vistoria no formato 'YYYY-MM-DD HH:MM:SS'
        status TEXT NOT NULL DEFAULT 'Pendente', -- Status: Pendente, Concluída, Cancelada
        FOREIGN KEY (imovel_id) REFERENCES imoveis (id),
        FOREIGN KEY (vistoriador_id) REFERENCES funcionarios (id)
    );

    -- Tabela de Agendamentos
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vistoria_id INTEGER NOT NULL,
        data TEXT NOT NULL, -- Data e horário do agendamento no formato 'YYYY-MM-DD HH:MM:SS'
        status TEXT NOT NULL DEFAULT 'Agendado', -- Status do agendamento
        FOREIGN KEY (vistoria_id) REFERENCES vistorias (id)
    );

    -- Tabela de Relatórios
    CREATE TABLE IF NOT EXISTS relatorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vistoria_id INTEGER NOT NULL,
        vistoriador_id INTEGER NOT NULL,
        texto TEXT NOT NULL, 
        data_geracao TEXT NOT NULL, -- Data de geração do relatório no formato 'YYYY-MM-DD HH:MM:SS'
        FOREIGN KEY (vistoria_id) REFERENCES vistorias (id),
        FOREIGN KEY (vistoriador_id) REFERENCES funcionarios (id)
    );

    -- Tabela de Fotos
    CREATE TABLE IF NOT EXISTS fotos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relatorio_id INTEGER NOT NULL, 
        dados BLOB NOT NULL, -- Conteúdo binário da imagem
        nome_arquivo TEXT NOT NULL, 
        FOREIGN KEY (relatorio_id) REFERENCES relatorios (id)
    );

    -- Tabela de Notificações
    CREATE TABLE IF NOT EXISTS notificacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL, -- Referência ao funcionário que recebe a notificação
        mensagem TEXT NOT NULL, -- Mensagem da notificação
        tipo TEXT NOT NULL, -- Tipo: ex.: 'Vistoria', 'Agendamento', etc.
        referencia_id INTEGER, -- ID do objeto relacionado (ex.: id da vistoria ou agendamento)
        data_criacao TEXT NOT NULL DEFAULT (DATETIME('now')), -- Data e hora de criação da notificação
        lida INTEGER NOT NULL DEFAULT 0, -- Status de leitura: 0 = Não Lida, 1 = Lida
        FOREIGN KEY (usuario_id) REFERENCES funcionarios (id)
    );
    '''

    # Executa o script SQL
    cursor.executescript(script_sql)

    # Confirma as mudanças e fecha a conexão
    conn.commit()
    conn.close()dara
    print("Tabelas criadas com sucesso!")

# Chama a função para criar as tabelas
criar_tabelas()
