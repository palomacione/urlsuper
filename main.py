from flask import *
import hashlib
from usuarios import *
from QrCode import *

app = Flask(__name__)  # cria novo app
usuarios = []
urls = []
long_short = {}
@app.route("/")
def main_page():
    return("Hello World")

@app.route("/usuarios", methods=["POST"])
def add_user():
    nome = request.json['nome']  
    nickname = request.json['nickname'] 
    email = request.json['email']
    senha_plain = request.json['senha'] 
    senha = hashlib.md5(senha_plain.encode())

    if any(x.email == email for x in usuarios):
        result = "Email já castrado"
        return result, 409
    elif any(x.nickname == nickname for x in usuarios):
        result = "Nickname já castrado"
        return result, 409
    else:
        usuario = Usuario(nome, nickname, email, senha)
        usuarios.append(usuario)
        result = "Usuário cadastrado com sucesso"
        return result, 201

@app.route("/qrcode", methods=["GET"])
def create_qrcode():
    return render_template("qrcode_upload.html")

@app.route("/success", methods=["POST"])
def show_qrcode():
    url = request.form['url']
    tamanho = request.form['tamanho']
    qrcode = QrCode.criarQrCode(url, tamanho)
    return redirect(qrcode), 200

@app.route("/cadastrarurl", methods=["POST"])    
def cadastrar():
    r_nickname = request.json['nickname']
    id = request.json['id']
    url = request.json['url']
    for x in usuarios:
        if r_nickname != x.nickname:
            return "Usuário não encontrado"
    else:
        for x in usuarios:
            if x.nickname == r_nickname:
                x.cadastrarUrl(id, url)
                return "Url cadastrada"

@app.route("/encurtar", methods= ["POST"])
def encurtar():
    r_nickname = request.json['nickname']
    id_ = request.json['id']
    url = request.json['url']
    for x in usuarios:
        if x.nickname != r_nickname:
            return "Usuário não encontrado"
        else:
            for x in usuarios:
                if x.nickname == r_nickname:
                    short_url = x.encurtarUrl(id_)
                    long_short[short_url] = url
                    return "Sua nova url é http://localhost:5000/u/{}".format(short_url) 

@app.route("/u/<id>", methods=["GET", "DELETE"])
def get_redirect(id):
    if id in long_short:
        if request.method == "GET":  
            for s, l in long_short.items():
                if s == id:
                    return redirect(l), 301
        else:
            del long_short[id]
            return "Url deletada"
    else:
        result = "Não há cadastros com essa url"
        return result
if __name__ == '__main__':
    app.run(debug=False)