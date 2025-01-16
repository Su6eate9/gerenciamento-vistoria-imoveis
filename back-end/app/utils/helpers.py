import sqlite3

def find_by_id(data_list, item_id):
    for item in data_list:
        if item.id == item_id:
            return item
    return None

def get_db_connection():
    #Cria e retorna uma conexão com o banco de dados SQLite.
    conn = sqlite3.connect('prototipo1.db') 
    conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários
    return conn
