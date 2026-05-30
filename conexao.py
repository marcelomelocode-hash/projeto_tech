import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "radartech",
}


def conectar():
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        print("Conectado ao MySQL com sucesso!")
        return conexao
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao:
        conexao.close()
        print("Conexão encerrada")


if __name__ == "__main__":
    minha_conexao = conectar()
    if minha_conexao:
        fechar_conexao(minha_conexao)
