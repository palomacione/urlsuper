class Initializer:
    def __init__(self, conn):
        self.createTableQrCode(conn)
        self.createTableCategoria(conn)
        self.createTableUrl(conn)
        self.createTableCategoriaUrl(conn)
        self.createTableUrlEncurtada(conn)
        self.creatTableUrl_Personalizada(conn)
        self.createTableUsuario(conn)
        conn.commit()
        conn.close()

    def createTableUrl(self, c):
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS Url
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_original TEXT,
                autor TEXT,
                qrcode INTEGER,
                FOREIGN KEY(autor) REFERENCES Usuario(nickname),
            FOREIGN KEY(qrcode) REFERENCES Qrcode(id) );
        """)

    def createTableUsuario(self, c):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS Usuario
                      (email TEXT UNIQUE,
                      nickname TEXT PRIMARY KEY,
                        nome TEXT,
                        senha TEXT,
                        foto BLOB,
                        acessos INTEGER);""")

    def creatTableUrl_Personalizada(self, c):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS UrlPersonalizada
                      (encurtamento TEXT,
                        url INTEGER PRIMARY KEY,
                      FOREIGN KEY(url) REFERENCES URL(id));
              """)

    def createTableUrlEncurtada(self, c):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS UrlEncurtada
                      (encurtamento TEXT,
                        url INTEGER PRIMARY KEY,
                      FOREIGN KEY(url) REFERENCES URL(id));
              """)

    def createTableCategoria(self, c):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS Categoria
                      (nome TEXT PRIMARY KEY,
                        acessos INTEGER);
              """)

    def createTableQrCode(self, c):
        c.execute(f"""
                  CREATE TABLE IF NOT EXISTS QrCode
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tamanho INTEGER,
                        imagem BLOB);
              """)

    def createTableCategoriaUrl(self, c):
        c.execute(f"""
                    CREATE TABLE IF NOT EXISTS CategoriaUrl
                        (url INTEGER PRIMARY KEY ,
                        categoria TEXT,
                        FOREIGN KEY(url) REFERENCES URL(id),
                        FOREIGN KEY(categoria) REFERENCES Categoria(nome));
                    """)





