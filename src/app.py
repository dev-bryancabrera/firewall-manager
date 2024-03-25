from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import subprocess
from flask_socketio import SocketIO, emit

from config import config
from router.routes import configurar_rutas

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
csrf = CSRFProtect()

app.config.from_object(config["development"])
login_manager_app = LoginManager(app)

configurar_rutas(app, login_manager_app)

block_all_command = ["sudo", "ufw", "default", "deny", "incoming"]
subprocess.run(block_all_command)
block_all_command = ["sudo", "ufw", "default", "deny", "outgoing"]
subprocess.run(block_all_command)


def status_401(error):
    return redirect(url_for("login"))


def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404


csrf.init_app(app)
app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)

if __name__ == "__main__":
    # csrf.init_app(app)
    # app.config.from_object(config["development"])
    app.run(host="0.0.0.0", port=3000)
