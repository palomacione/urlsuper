from flask import *
import bcrypt
from PIL import Image
from models import *
from main import Fachada

app = Flask(__name__)
# usuarios = []
# urls = []
# long_short = {}

f = Fachada.get_instance()
def procurar_usuario(nick):
    user = None
    for x in usuarios:
        if x.getNick() == nick:
            return x
    return user
def autenticar_usuario(senha_plain, senha_hashed):
    return True
    # return bcrypt.checkpw(senha_hashed, senha_plain)

def procurar_url(user, url_):
    url = None
    for u in user.getUrls():
        if u.getUrl() == url_:
            return u
    return url

@app.route("/")
def main_page():
    return render_template("home.html")

@app.route("/usuarios", methods=["POST"])
def add_user():
    nome = request.form['nome']
    nickname = request.form['nickname']
    email = request.form['email']
    senha_plain = request.form['senha']
    senha_plain = senha_plain.encode(encoding='UTF-8')
    salt = bcrypt.gensalt()
    senha = bcrypt.hashpw(senha_plain, salt)

    usuario = Usuario(nome, nickname, email, senha)
    result = f.put(usuario)
    return result, 200

@app.route("/qrcode", methods=["GET"])
def create_qrcode():
    return render_template("qrcode_upload.html")

@app.route("/success", methods=["POST"])
def show_qrcode():
    url = request.form['url']
    tamanho = request.form['tamanho']
    qrcode = QrCode.criarQrCode(url, tamanho)
    return redirect(qrcode)

@app.route("/cadastrarurl", methods = ["GET"])
def cadastrar():
    return render_template("cadastrarUrl.html")

@app.route("/urls", methods=["POST"])
def cadastrarUrl():
    r_nickname = request.form['nickname']
    url = request.form['url']
    senha_plain = request.form['senha']
    usuario = f.get(r_nickname, "Usuario")
    if usuario is not None:
        nickname = usuario[0][0]
        senha = str(usuario[0][1])
        senha_plain = senha_plain.encode(encoding='UTF-8')
        if autenticar_usuario(senha, senha_plain):
            url = Url(url, nickname)
            f.put(url)
            return "Url Cadastrada com sucesso"
        else:
            return "Senha errada"
    else:
        return "Usuário não encontrado"


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


@app.route("/cadastro", methods=['GET'])
def login():
    return render_template("cadastro.html")

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
    if user is not None:
        url =  procurar_url(user, r_url)
        if autenticar_usuario(user, senha): 
            if url is not None:
                if url in user.encurtadas:
                    if texto == user.encurtadas[url].getPersonalização():
                        return "Você já possui uma url com essa personalização"
                    else:
                        new = urllib.parse.quote(texto)
                        user.encurtadas[url].personalização = new
                        return "Sua url personalizada é http://localhost:5000/{}/{}".format(r_nickname, new)
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
            if width > 500 or height > 500 or img.format != "png":
                return "Imagem fora dos padrões, a imagem deve ser no máximo 500x500, png ou jpeg"
            else:
                return "Sucesso"
        else:
            return "Senha incorreta, tente novamente"
    else:
        return "Usuário não encontrado"

@app.route("/categorizar", methods =['GET'])
def categorizar():
    return render_template("categorizar.html")

@app.route("/categorias", methods=["POST"])
def categorias():
    r_nickname = request.form['nickname']
    senha_plain = request.form['senha']
    url = request.form['url']
    nome = request.form['nome']
    usuario = f.get(r_nickname, "Usuario")
    if usuario is not None:
        nickname = usuario[0][0]
        senha = str(usuario[0][1])
        senha_plain = senha_plain.encode(encoding='UTF-8')
        if autenticar_usuario(senha, senha_plain):
            cat = f.get(nome, "Categoria")
            if cat is None:
                categoria = Categoria(nome)
                f.put(categoria)
            url = Url(url, nickname)
            id = f.get(url, "Url")
            if id is not None:
                id = id[0][0]
                catUrl = CategoriaUrl(id, nome)
                obj = f.put(catUrl)
            else:
                return "Url não encontrada"
            return obj
        else:
            "Senha incorreta"
    else:
        "Usuário não encontrado"