from database import Initializer
import sqlite3


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

    def select(self, valor, c):
        # try:
        c.execute("""SELECT nickname, senha
                      FROM Usuario 
                      WHERE nickname = '{}'""".format(valor))
        obj = c.fetchall()
        return obj
        # except:
        #     return None

    def remove(self, objUser, c):
        c.execute("DELETE FROM Usuario WHERE nickname = {}".format(objUser.nickname))

    def update(self, objUser, field, c):
        c.execute("UPDATE Usuario SET {} = {} WHERE nickname = {}".format(field, objUser.field, objUser.nickname))

    def insert(self, objUser, c):
        try:
            c.execute("""INSERT INTO Usuario (email, nickname, nome, senha)
                            VALUES ("{}","{}","{}","{}")""".format(objUser.email, objUser.nickname, objUser.nome,
                                                                   objUser.senha))
            return "Usuário cadastrado com sucesso"
        except sqlite3.IntegrityError:
            return "Nickname ou email já cadastrado"


class MapeadorURl(Interface):

    def select(selfself, objUrl, c):
        try:
            c.execute("SELECT id FROM Url WHERE url_original = '{}' and autor = '{}'".format(objUrl.url, objUrl.nickname))
            id = c.fetchall()
            return id
        except:
            return None

    def remove(self, objUrl, c):
        c.execute("DELETE FROM Url WHERE id = {}".format(objUrl.id))

    def update(self, objUrl, field, c):
        c.execute("UPDATE URL SET {} = {} WHERE id = {}".format(field, objUrl.field, objUrl.id))

    def insert(self, objUrl, c, objQrCode = None):
        if objQrCode is not None:
            c.execute("""INSERT INTO Url (url_original, autor, qrcode) 
                        VALUES ('{}','{}','{}')""".format(objUrl.url, objUrl.nickname, objQrCode.id))
        else:
            c.execute("""INSERT INTO Url (url_original, autor) 
                                    VALUES ('{}','{}')""".format(objUrl.url, objUrl.nickname))

class MapeadorURlPersonalizada(Interface):

    def select(selfself, objUrlPersonalizada,c):
        c.execute("SELECT * FROM UrlPersonalizada WHERE personalizacao = {}".format(objUrlPersonalizada.personalizacao))

    def remove(self, objUrlPersonalizada,c):
        c.execute("DELETE FROM UrlPersonalizada WHERE personalizacao = {}".format(objUrlPersonalizada.personalizacao))


    def update(self, objUrlPersonalizada, field, c):
        c.execute(
            "UPDATE URLPersonalizada SET {} = {} WHERE personalizacao = {}".format(field, objUrlPersonalizada.field,
                                                                                   objUrlPersonalizada.personalizacao))

    def insert(self, objUrl, objUrlPersonalizada, c):
        c.execute("""INSERT INTO UrlPersonalizada (personalizacao, url) 
                                VALUES ({},{})""".format(objUrlPersonalizada.personalizacao, objUrl.id))


class MapeadorUrlEncurtada(Interface):

    def select(selfself, objUrlEncurtada, c):
        c.execute("SELECT * FROM UrlEncurtada WHERE encurtamento = {}".format(objUrlEncurtada.encurtamento))

    def remove(self, objUrlEncurtada, c):
        c.execute("DELETE FROM UrlEncurtada WHERE encurtamento = {}".format(objUrlEncurtada.encurtamento))

    def update(self, objUrlEncurtada, field, c):
        c.execute("UPDATE URLEncurtada SET {} = {} WHERE encurtamento = {}".format(field, objUrlEncurtada.field,
                                                                                   objUrlEncurtada.encurtamento))

    def insert(self, objUrl, objUrlEncurtada, c):
        c.execute("""INSERT INTO UrlEncurtada (encurtamento, url) 
                                VALUES ({},{})""".format(objUrlEncurtada.encurtamento, objUrl.id))


class MapeadorQrCode(Interface):

    def select(selfself, objQrCode, c):
        c.execute("SELECT * FROM QrCode WHERE id = {}".format(objQrCode.id))

    def remove(self, objQrCode, c):
        c.execute("DELETE FROM QrCode WHERE id = {}".format(objQrCode.id))

    def update(self, objQrCode, field, c):
        c.execute("UPDATE QrCode SET {} = {} WHERE id = {}".format(field, objQrCode.field, objQrCode.id))

    def insert(self, objQrCode, c):
        c.execute("""INSERT INTO QrCode (tamanho, imagem) 
                                VALUES ({},{})""".format(objQrCode.tamanho, objQrCode.imagem))


class MapeadorCategoria(Interface):

    def select(self, nome, c):
        try:
            c.execute("SELECT nome FROM Categoria WHERE nome = '{}'".format(nome))
            return 1
        except:
            return None

    def remove(self, objCategoria, c):
        c.execute("DELETE FROM Categoria WHERE id = {}".format(objCategoria.nome))

    def update(self, objCategoria, field, c):
        c.execute("UPDATE Categoria SET {} = {} WHERE id = {}".format(field, objCategoria.field, objCategoria.nome))

    def insert(self, objCategoria, c):
        c.execute("""INSERT INTO Categoria (nome, acessos) 
                                VALUES ('{}',{})""".format(objCategoria.nome, objCategoria.acessos))


class MapeadorCategoriaUrl(Interface):

    def select(selfself, objUrl, c):
        c.execute("SELECT * FROM CategoriaUrl WHERE id = {}".format(objUrl.id))

    def remove(self, objUrl, c):
        c.execute("DELETE FROM CategoriaUrl WHERE id = {}".format(objUrl.id))

    def update(self, objCategoria, field, c):
        c.execute("UPDATE CategoriaUrl SET {} = {} WHERE id = {}".format(field, objCategoria.field, objCategoria.nome))

    def insert(self, objCategoriaUrl, c):
        print(objCategoriaUrl.categoria, objCategoriaUrl.url)
        try:
            c.execute(f"""INSERT INTO CategoriaUrl (url, categoria)
                        VALUES ({objCategoriaUrl.url},'{objCategoriaUrl.categoria}')""")
            return "Categoria adicionada com sucesso"
        except sqlite3.IntegrityError:
            return "Essa categoria já foi adicionada para essa url"


mapping = {"Url": MapeadorURl, "Usuario": MapeadorUsuario, "Categoria": MapeadorCategoria,
           "UrlPersonalizada": MapeadorURlPersonalizada, "UrlEncurtada": MapeadorUrlEncurtada,
           "CategoriaUrl": MapeadorCategoriaUrl}


class Fachada:
    def __init__(self):
        conn = sqlite3.connect("database.db", check_same_thread=False)
        Initializer(conn)

    def get_instance(self):
        f = Fachada()
        return f

    def get(self, valor, obj):
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c = conn.cursor()
        m = mapping[obj]()
        obj = m.select(valor, c)
        conn.commit()
        c.close()
        return obj

    def put(self, obj):
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c = conn.cursor()
        tipoMapeador = type(obj).__name__
        m = mapping[tipoMapeador]()
        obj = m.insert(obj, c)
        conn.commit()
        c.close()
        return obj

    def remove(self, obj):
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c = conn.cursor()
        tipoMapeador = type(obj).__name__
        m = mapping[tipoMapeador]()
        m.remove(obj, c)
        conn.commit()
        c.close()

    def update(self, field, obj):
        conn = sqlite3.connect("database.db", check_same_thread=False)
        c = conn.cursor()
        tipoMapeador = type(obj).__name__
        m = mapping[tipoMapeador]()
        m.update(field, obj, c)
        conn.commit()
        c.close()