from algorithm import *
import urllib.parse


class Usuario:
    def __init__(self, nome, nickname, email, senha, encurtadas = {}, foto = None, acessos = 0):
        self.nome = nome
        self.nickname = nickname
        self.email = email
        self.senha = senha
        self.urls = []
        self.encurtadas = encurtadas
        self.foto = foto
        self.acessos = acessos
    def cadastrarUrl(self, id_, url):
        self.urls.append(Url(id_, url))
    
    def encurtarUrl(self, id_):
        short_url = encode(int(id_))
        return short_url
    
    def getSenha(self):
        return self.senha

    def getNick(self):
        return self.nickname
    
    def getUrls(self):
        return self.urls


class Url:
    def __init__(self, url, nickanme, qrcode = None):
        self.url = url
        self.nickname = nickanme
        self.qrcode = qrcode
    
    def getUrl(self):
        return self.url


class CategoriaUrl:
    def __init__(self, url, categoria):
        self.url = url
        self.categoria = categoria


class UrlPersonalizada(Url):
    def __init__(self, id, url, personalização):
        self.id = id
        self.url = url
        self.personalização = personalização
    
    def getPersonalização(self):
        return self.personalização


class QrCode:
    def __init__(self, url, tamanho):
        self.url = url
        self.tamanho = str(tamanho)
    
    def criarQrCode(url, tamanho):
        data = urllib.parse.quote(url)
        qrcode = 'https://api.qrserver.com/v1/create-qr-code/?data={}&size={}x{}'.format(data, tamanho, tamanho)
        return qrcode


class UrlEncurtada(Url):
    def __init__(self, url, encurtamento):
        self.encurtamento = encurtamento
        self.url = url


class Categoria:
    def __init__(self, nome, acessos = 0):
        self.nome = nome
        self.acessos = acessos

