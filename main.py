from flask import *
from views import app
from mapeadores import Fachada
if __name__ == '__main__':
    Fachada()
    app.run(debug=False)