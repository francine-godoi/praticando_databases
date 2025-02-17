from sqlite3 import IntegrityError
from config import TABELA_USUARIOS
from models.usuarios import Usuario
from database.auxiliar_db_sql import AuxiliarDB


class RepositorioUsuario(AuxiliarDB):


    def __init__(self) -> None:
        self.criar_tabela_usuario()

    def criar_tabela_usuario(self) -> None:
        sql = f"""CREATE TABLE IF NOT EXISTS {TABELA_USUARIOS} (
                    id_usuario INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    salt TEXT NOT NULL
        )"""

        self.executar_sql(sql)
        self.fechar_conexao()

    def cadastrar_usuario(self, usuario: Usuario) -> int:

        sql = f"""INSERT INTO {TABELA_USUARIOS} (username, senha, salt) VALUES (?,?,?)"""

        info_usuario = (usuario.username, usuario.senha, usuario.salt)
        try:
            resultado = self.executar_sql(sql, info_usuario, comitar=True).rowcount
            self.fechar_conexao()
            return resultado
        except IntegrityError:
            self.fechar_conexao()
            return 0

    def selecionar_usuario_por_username(self, username: str) -> Usuario | int:

        sql = f"""SELECT * FROM {TABELA_USUARIOS} WHERE username = ?"""

        resultado = self.executar_sql(sql, (username,)).fetchone()
        self.fechar_conexao()

        if not resultado:
            return 0
        # 1 = username, 2 = senha, 3 = salt, 1 = id_usuario
        usuario = Usuario(resultado[1], resultado[2], resultado[3], resultado[0])

        return usuario
