from urls import *
from algorithm import *
class Usuario:
    def __init__(self, nome, nickname, email, senha):
        self.nome = nome
        self.nickname = nickname
        self.email = email
        self.senha = senha
        self.urls = []

    def cadastrarUrl(self, id, url):
        self.urls.append(Url(id, url))
    
    def encurtarUrl(self, id):
        short_url = encode(int(id))
        return short_url
