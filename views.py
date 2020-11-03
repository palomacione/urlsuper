from flask import *
import bcrypt
from PIL import Image
from models import *

app = Flask(__name__) 
usuarios = []
urls = []
long_short = {}

def procurar_usuario(nick):
    user = None
    for x in usuarios:
        if x.getNick() == nick:
            return x
    return user
        
def autenticar_usuario(Usuario, senha):
    return bcrypt.checkpw(senha, Usuario.getSenha())

def procurar_url(user, url_):
    url = None
    for u in user.getUrls():
        if u.getUrl() == url_:
            return u
    return url

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
    if procurar_usuario(nickname) is not None:
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
    id_ = request.json['id']
    url = request.json['url']
    user = procurar_usuario(r_nickname)
    if user is not None:
        user.cadastrarUrl(id_, url)
        return "Url cadastrada"
    else:
        return "Usuário não cadastrado"

@app.route("/encurtar", methods= ["POST"])
def encurtar():
    r_nickname = request.json['nickname']
    id_ = request.json['id']
    url = request.json['url']
    user = procurar_usuario(r_nickname)
    if user is not None:
        short_url = user.encurtarUrl(id_)
        long_short[short_url] = url
        return "Sua nova url é http://localhost:5000/{}/{}".format(r_nickname, short_url) 
    else:
        return "Usuário não encontrado"


@app.route("/<user>/<id_>", methods=["GET", "DELETE"])
def get_redirect(user, id_):
    if id_ in long_short:
        if request.method == "GET":  
            for s, l in long_short.items():
                if s == id_:
                    return redirect(l), 301
        else:
            del long_short[id_]
            return "Url deletada"
    elif True:
        user_ = procurar_usuario(user)
        if user_ is not None:
            for l, p in user_.encurtadas.items():
                if p.getPersonalização() == id_:
                    url = l.getUrl()
                    return redirect(url)
        else:
            return "Usuário não encontrado"
    else:
        return "Não há cadastros com essa url"

@app.route("/personalizar",methods = ['POST', 'GET'])
def personalizar():
    return render_template("personalizarUrl.html")

@app.route("/check", methods=["POST"])
def personalizar_url():
    r_url = request.form['url']
    r_nickname = request.form['Nickname']
    senha = request.form['Senha']
    senha = senha.encode(encoding='UTF-8')
    texto = request.form['Texto']
    new = ''
    user = procurar_usuario(r_nickname)
    url =  procurar_url(user, r_url)
    if user is not None:
        if autenticar_usuario(user, senha): 
            if url is not None:
                if url in user.encurtadas:
                    if texto == user.encurtadas[url].personalização:
                        return "Você já possui uma url com essa personalização"
                else:
                    new = urllib.parse.quote(texto)
                    urlP = UrlPersonalizada(url.getId(), url.getUrl(), new)
                    user.encurtadas[url] = urlP
                    return "Sua url personalizada é http://localhost:5000/{}/{}".format(r_nickname, new)
            else:
                return "Url não cadastrada"
        else:
            return "Senha errada, tente novamente"
    else:
        return "Usuário não encontrado"

@app.route('/trocarfoto', methods = ["GET"])
def trocar_foto():
    return render_template("trocar_foto.html")

@app.route("/checksize", methods = ["POST"])
def verificar_tamanho():
    foto = request.files.get('foto', '')
    r_nickname = request.form['Nickname']
    senha = request.form['Senha']
    senha = senha.encode(encoding='UTF-8')
    user = procurar_usuario(r_nickname)
    if user is not None:
        if autenticar_usuario(user, senha):
            img = Image.open(foto)
            width, height = img.size
            if width > 500 or height > 500:
                return "Imagem fora dos padrões, a imagem deve ser no máximo 500x500, png ou jpeg"
            else:
                return "Sucesso"
            if img.format != "png" and img.format != "jpeg":
                return "Imagem fora dos padrões, a imagem deve ser no máximo 500x500, png ou jpeg"
        else:
            return "Senha incorreta, tente novamente"
    else:
        return "Usuário não encontrado"