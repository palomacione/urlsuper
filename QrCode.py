import urllib.parse
import requests
class QrCode:
    def __init__(self, url, tamanho):
        self.url = url
        self.tamanho = str(tamanho)
    
    def criarQrCode(url, tamanho):
        data = urllib.parse.quote(url)
        qrcode = 'https://api.qrserver.com/v1/create-qr-code/?data={}&size={}x{}'.format(data, tamanho, tamanho)
        return qrcode
