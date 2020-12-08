import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
mapping = {"Url": MapeadorURl, "Usuario": MapeadorUsuario, "Categoria": MapeadorCategoria,
            "UrlPersonalizada": MapeadorURlPersonalizada, "UrlEncurtada": MapeadorUrlEncurtada}  # Cada objeto terá seu Mapeador

class Fachada:
    def get(self, obj):
        # tipoMapeador = type(obj).__class__
        pass
    def put(self, obj):
        tipoMapeador = type(obj).__class__
        m = mapping[tipoMapeador]()
        m.insert(obj)
    def remove(self, obj):
        tipoMapeador = type(obj).__class__
        m = mapping[tipoMapeador]()
        m.remove(obj)
    def update(self, field, obj):
        tipoMapeador = type(obj).__class__
        m = mapping[tipoMapeador]()
        m.update(field, obj)

class Interface:
    def __init__(self):
        pass
    def MapeadorUsuario(self):
        pass
    def MapeadorUrl(self):
        pass
    def MapeadorCategoria(self):
        pass
    def MapeadorUrlPersonalizada(self):
        pass
    def MapeadorUrlEncurtada(self):
        pass
    def MapeadorCategoriaUrl(self):
        pass
    def MapearQrode(self):
        pass

class MapeadorUsuario(Interface):

    def select(self, objUser):
        c.execute("SELECT * FROM USUARIO WHERE nickname = {}".format(objUser.nickname))

    def remove(self, objUser):
        c.execute("DELETE FROM USUARIO WHERE nickname = {}".format(objUser.nickname))

    def update(self,objUser, field):
        c.execute("UPDATE USUARIO SET {} = {} WHERE nickname = {}".format(field, objUser.field, objUser.nickname))

    def insert(self, objUser):
        c.execute("""INSERT INTO USUARIO (email, nickname, nome, senha, foto, acessos)
                        VALUES ({},{},{},{},{},{})""".format(objUser.email, objUser.nickname, objUser.nome, objUser.senha, objUser.foto, objUser.acessos))

class MapeadorURl(Interface):

    def select(selfself, objUrl):
        c.execute("SELECT * FROM URL WHERE id = {}".format(objUrl.id))

    def remove(self, objUrl):
        c.execute("DELETE FROM URL WHERE id = {}".format(objUrl.id))

    def update(self, objUrl, field, value):
        c.execute("UPDATE URL SET {} = {} WHERE id = {}".format(field, objUrl.field, objUrl.id))

    def insert(self, objUrl, objUser, objQrCode):
        if objQrCode is not None:
            conn.execute("""INSERT INTO URL (url_original, autor, qrcode) 
                        VALUES ({},{},{})""".format(objUrl.url_original, objUser.nickname, objQrCode.id))
        else:
            conn.execute("""INSERT INTO URL (url_original, autor) 
                                    VALUES ({},{})""".format(objUrl.url_original, objUser.nickname)

class MapeadorURlPersonalizada(Interface):

    def select(selfself, objUrlPersonalizada):
        c.execute("SELECT * FROM UrlPersonalizada WHERE personalizacao = {}".format(objUrlPersonalizada.personalizacao))

    def remove(self, objUrlPersonalizada):
        c.execute("DELETE FROM UrlPersonalizada WHERE personalizacao = {}".format(objUrlPersonalizada.personalizacao))

    def update(self, objUrlPersonalizada, field):
        c.execute("UPDATE URLPersonalizada SET {} = {} WHERE personalizacao = {}".format(field, objUrlPersonalizada.field, objUrlPersonalizada.personalizacao))

    def insert(self, objUrl, objUrlPersonalizada):
        c.execute("""INSERT INTO UrlPersonalizada (personalizacao, url) 
                                VALUES ({},{})""".format(objUrlPersonalizada.personalizacao, objUrl.id))

class MapeadorUrlEncurtada(Interface):

    def select(selfself, objUrlEncurtada):
        c.execute("SELECT * FROM UrlEncurtada WHERE encurtamento = {}".format(objUrlEncurtada.encurtamento))

    def remove(self, objUrlEncurtada):
        c.execute("DELETE FROM UrlEncurtada WHERE encurtamento = {}".format(objUrlEncurtada.encurtamento))

    def update(self, objUrlEncurtada, field):
        c.execute("UPDATE URLEncurtada SET {} = {} WHERE encurtamento = {}".format(field, objUrlEncurtada.field, objUrlEncurtada.encurtamento))

    def insert(self, objUrl, objUrlEncurtada):
        c.execute("""INSERT INTO UrlEncurtada (encurtamento, url) 
                                VALUES ({},{})""".format(objUrlEncurtada.encurtamento, objUrl.id))

class MapeadorQrCode(Interface):

    def select(selfself, objQrCode):
        c.execute("SELECT * FROM QrCode WHERE id = {}".format(objQrCode.id))

    def remove(self, objQrCode):
        c.execute("DELETE FROM QrCode WHERE id = {}".format(objQrCode.id))

    def update(self, objQrCode, field):
        c.execute("UPDATE QrCode SET {} = {} WHERE id = {}".format(field, objQrCode.field, objQrCode.id))

    def insert(self, objQrCode):
        c.execute("""INSERT INTO QrCode (tamanho, imagem) 
                                VALUES ({},{})""".format(objQrCode.tamanho, objQrCode.imagem))

class MapeadorCategoria(Interface):

    def select(selfself, objCategoria):
        c.execute("SELECT * FROM Categoria WHERE nome = {}".format(objCategoria.nome))

    def remove(self, objCategoria):
        c.execute("DELETE FROM Categoria WHERE id = {}".format(objCategoria.nome))

    def update(self, objCategoria, field):
        c.execute("UPDATE Categoria SET {} = {} WHERE id = {}".format(field, objCategoria.field, objCategoria.nome))

    def insert(self, objCategoria):
        c.execute("""INSERT INTO QrCode (nome, acessos) 
                                VALUES ({},{})""".format(objCategoria.nome, objCategoria.acessos))

class MapeadorCategoriaUrl(Interface):

    def select(selfself, objUrl):
        c.execute("SELECT * FROM CategoriaUrl WHERE id = {}".format(objUrl.id))

    def remove(self, objUrl):
        c.execute("DELETE FROM CategoriaUrl WHERE id = {}".format(objUrl.id))

    def update(self, objCategoria, field):
        c.execute("UPDATE CategoriaUrl SET {} = {} WHERE id = {}".format(field, objCategoria.field, objCategoria.nome))

    def insert(self, objUrl, objCategoria):
        c.execute("""INSERT INTO CategoriaUrl (url, categoria)
                        VALUES ({},{})""".format(objUrl.id, objCategoria.nome))


