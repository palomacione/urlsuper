from algorithm import *
import urllib.parse


class Usuario:
    def __init__(self, nome, nickname, email, senha, encurtadas = {}, foto = None):
        self.nome = nome
        self.nickname = nickname
        self.email = email
        self.senha = senha
        self.urls = []
        self.encurtadas = encurtadas
        self.foto = foto

    def cadastrarUrl(self, id, url, categoria = ''):
        self.urls.append(Url(id, url))
    
    def encurtarUrl(self, id):
        short_url = encode(int(id))
        return short_url
        
class Url:
    def __init__(self, id, url, acessos = 0):
        self.url = url
        self.acessos = acessos

class QrCode:
    def __init__(self, url, tamanho):
        self.url = url
        self.tamanho = str(tamanho)
    
    def criarQrCode(url, tamanho):
        data = urllib.parse.quote(url)
        qrcode = 'https://api.qrserver.com/v1/create-qr-code/?data={}&size={}x{}'.format(data, tamanho, tamanho)
        return qrcode
