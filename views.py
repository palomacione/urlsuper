from flask import *
import bcrypt
from PIL import Image
from models import *

app = Flask(__name__) 
usuarios = []
urls = []
long_short = {}


@app.route("/")
def main_page():
    return("URLSuper")

@app.route("/usuarios", methods=["POST"])
def add_user():
    nome = request.json['nome']  
    nickname = request.json['nickname'] 
    email = request.json['email']
    senha_plain = request.json['senha'] 
    senha_plain = senha_plain.encode(encoding='UTF-8')
    salt = bcrypt.gensalt()
    senha = bcrypt.hashpw(senha_plain, salt)

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
    return redirect(qrcode)

@app.route("/cadastrarurl", methods=["POST"])    
def cadastrar():
    r_nickname = request.json['nickname']
    id = request.json['id']
    url = request.json['url']
    if any(x.nickname == nickname for x in usuarios):
        x.cadastrarUrl(id, url)
        return "Url cadastrada"
    else:
        return "Usuário não cadastrado"

@app.route("/encurtar", methods= ["POST"])
def encurtar():
    r_nickname = request.json['nickname']
    id_ = request.json['id']
    url = request.json['url']
    if any(x.nickname == r_nickname for x in usuarios):
        short_url = x.encurtarUrl(id_)
        long_short[short_url] = url
        return "Sua nova url é http://localhost:5000/{}/{}".format(r_nickname, short_url) 
    else:
        return "Usuário não encontrado"


@app.route("/<user>/<id>", methods=["GET", "DELETE"])
def get_redirect(user, id):
    if id in long_short:
        if request.method == "GET":  
            for s, l in long_short.items():
                if s == id:
                    return redirect(l), 301
        else:
            del long_short[id]
            return "Url deletada"
    elif True:
        for x in usuarios:
            if x.nickname == user:
                user = x
                break
            else:
                return "Usuário não encontrado"
        for l, p in user.encurtadas.items():
            if p == id:
                return redirect(l)
    else:
        return "Não há cadastros com essa url"

@app.route("/p/<nick>/<id>", methods=["GET", "DELETE"])
def r(nick, id):
    for x in usuarios:
        if x.nickname == nick:
            for l, p in x.encurtadas.items():
                if p == id:
                    return redirect(l)

@app.route("/personalizar",methods = ['POST', 'GET'])
def personalizar_url():
    return render_template("personalizarUrl.html")

@app.route("/check", methods=["POST"])
def verificar_texto():
    url = request.form['url']
    r_nickname = request.form['Nickname']
    senha = request.form['Senha']
    senha = senha.encode(encoding='UTF-8')
    texto = request.form['Texto']
    new = ''

    for x in usuarios:
        if x.nickname == r_nickname:
            user = x
            break
        else:
            return "Usuário não encontrado, tente novamente"

    if bcrypt.checkpw(senha, user.senha):
        if url in user.encurtadas:
            if texto in user.encurtadas.values():
                return "Você já possui uma url com essa personalização"
        else:
            new = urllib.parse.quote(texto)
            user.encurtadas[url] = new
            return "Sua url personalizada é http://localhost:5000/{}/{}".format(r_nickname, new)
    else:
        return "Senha errada, tente novamente"

@app.route('/trocarfoto', methods = ["GET"])
def trocar_foto():
    return render_template("trocar_foto.html")

@app.route("/checksize", methods = ["POST"])
def verificar_tamanho():
    foto = request.files.get('foto', '')
    r_nickname = request.form['Nickname']
    senha = request.form['Senha']
    senha = senha.encode(encoding='UTF-8')
    user = None
    for x in usuarios:
        if x.nickname == r_nickname:
            user = x
            break
        else:
            return "Usuário não encontrado, tente novamente"

    img = Image.open(foto)
    width, height = img.size
    if width > 500 or height > 500:
        return "Imagem fora dos padrões, a imagem deve ser no máximo 200x200"
    else:
        if bcrypt.checkpw(senha, user.senha):
            user.foto = img
            return "Sucesso"
        else:
            return "Senha incorreta, tente novamente"