import mysql.connector

TABELA_CADASTRO = "tbl_cadastro"

_SESSION_STORE: dict[str, str] = {}

class _SessionCompat:
    def __init__(self):
        self._data: dict[str, str] = {}

    def get(self, key: str, default=None):
        try:
            return _SESSION_STORE.get(key, default)
        except Exception:
            return default

    def set(self, key: str, value):
        _SESSION_STORE[key] = value

def get_session_store():
    return _SessionCompat()

def get_db_connection(include_database=True):
    config = {
        "host": "localhost",
        "user": "root",
        "password": "root"
    }
    if include_database:
        config["database"] = "radartech"
    return mysql.connector.connect(**config)

def init_db():
    conn = get_db_connection(include_database=False)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS radartech;")
    conn.commit()
    cursor.close()
    conn.close()
    
    conn = get_db_connection(include_database=True)
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABELA_CADASTRO} (
        id_cadastro INT AUTO_INCREMENT PRIMARY KEY,
        nome_completo VARCHAR(100),
        email_usuario VARCHAR(100),
        telefone_usuario VARCHAR(20),
        senha_usuario VARCHAR(100),
        aceitar_termos TINYINT,
        perfil_id INT,
        curso VARCHAR(100),
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        jornada VARCHAR(100),
        interesses VARCHAR(255)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def validate_login(email, senha):
    conn = get_db_connection(include_database=True)
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT id_cadastro FROM {TABELA_CADASTRO} WHERE email_usuario = %s AND senha_usuario = %s",
            (email, senha),
        )
        resultado = cursor.fetchone()
        return resultado is not None
    except Exception as e:
        print(f"Erro ao validar login: {e}")
        return False
    finally:
        cursor.close()
        conn.close()