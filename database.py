import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

class Initializer:

    def createTableUrl(self):
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS Url
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_original TEXT,
                FOREIGN KEY(autor) REFERENCES Usuario(nickname),
            FOREIGN KEY(qrcode) REFERENCES Qrcode(id) )
        """)

    def createTableUsuario(self):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS Usuario
                      (email TEXT PRIMARY KEY,
                      nickname INTEGER PRIMARY KEY,
                        nome TEXT,
                        senha TEXT,
                        foto BYTEA,
                        acessos INTEGER)""")

    def creatTableUrl_Personalizada(self):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS UrlPersonalizada
                      (encurtamento TEXT,
                        url INTEGER PRIMARY KEY
                      FOREIGN KEY(url) REFERENCES URL(id),
              """)

    def createTableUrlEncurtada(self):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS UrlEncurtada
                      (encurtamento TEXT,
                        url INTEGER PRIMARY KEY
                      FOREIGN KEY(url) REFERENCES URL(id),
              """)

    def createTableCategoria(self):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS Categoria
                      (nome TXT PRIMARY KEY,
                        acessos INTEGER PRIMARY KEY
              """)

    def createTableQrCode(self):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS QrCode
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tamanho INTEGER PRIMARY KEY,
                        imagem BYTEA
              """)

    def createTableCategoriaUrl(self):
        c.execute(f"""
                    CREATE TABLE IF NOT EXISTS CategoriaUrl
                        (url INTEGER PRIMARY KEY ,
                        categoria TEXT PRIMARY KEY
                        FOREIGN KEY(url) REFERENCES URL(id)
                        FOREIGN KEY(categoria) REFERENCES Categoria(nome)
                    """)

    def __init__(self):
        self.createTableQrCode()
        self.createTableCategoria()
        self.createTableUrl()
        self.createTableCategoriaUrl()
        self.createTableUrlEncurtada()
        self.creatTableUrl_Personalizada()
        self.createTableUsuario()
        conn.close()
        c.close()



