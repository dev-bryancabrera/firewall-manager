import json
from operator import truediv
import re
import subprocess
from flask import Response, redirect, render_template, jsonify, request, url_for
from scapy.all import sniff, IP, TCP
from datetime import datetime
from flask_login import logout_user, login_required

# Models
from models.modelUser import modelUser

from models.funciones import (
    obtener_reglas_ufw,
    delete_rule,
    scan_network,
    allow_connections,
    validar_ingreso,
    start_capture,
    pre_start_capture,
    deactivate_activate_rule,
)


def configurar_rutas(app, login_manager_app):

    @app.route("/")
    def login_user():
        return redirect(url_for("login"))

    @login_manager_app.user_loader
    def load_user(id):
        return modelUser.getById(id)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        try:
            if request.method == "POST":
                username = request.form.get("username")
                password_hash = request.form.get("password_hash")

                if validar_ingreso(username, password_hash):
                    return redirect(url_for("home_page"))
                else:
                    return render_template(
                        "login.html", error="Nombre de usuario o contraseña incorrectos"
                    )
            else:
                return render_template("login.html")

        except KeyError as e:
            return f"Error al iniciar sesion."

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/home")
    @login_required
    def home_page():
        return render_template("home-page.html")

    @app.route("/packets")
    @login_required
    def dashboard_page():
        devices = scan_network()
        return render_template("traffic-packets.html", devices=devices)

    @app.route("/ufw_manager")
    @login_required
    def obtener_reglas_ufw_route():

        devices = scan_network()

        resultado = obtener_reglas_ufw()

        if isinstance(resultado, tuple) and len(resultado) == 2:
            reglas_in, reglas_out = obtener_reglas_ufw()

            if "error" in reglas_in[0]:
                mensaje_error = reglas_in[0]["error"]
                return render_template("config-firewall.html", error=mensaje_error)

            if "error" in reglas_out[0]:
                mensaje_error = reglas_out[0]["error"]
                return render_template("config-firewall.html", error=mensaje_error)

            return render_template(
                "config-firewall.html",
                reglas_in=reglas_in,
                reglas_out=reglas_out,
                devices=devices,
            )
        else:
            mensaje_error = "Error al obtener las reglas UFW."
            return render_template("config-firewall.html", error=mensaje_error)

    is_capture_paused = False

    @app.route("/play-pause-cpacket", methods=["POST"])
    def toggle_play_pause():
        global is_capture_paused

        is_paused = request.form.get("isPaused")

        # Actualiza el estado de pausa según el valor recibido
        if is_paused == "true":
            is_capture_paused = True
            print("La captura de paquetes ha sido pausada.")
        else:
            is_capture_paused = False
            print("La captura de paquetes ha sido reanudada.")

        return "Acción de pausa/reanudación recibida."

    form_data = {}

    @app.route("/packetdata", methods=["GET", "POST"])
    def packet_data():
        global form_data
        global is_capture_paused

        if request.method == "POST":

            form_data = {}

            form_data = {
                "ip_addr": request.form.get("ip_addr"),
                "ip_dest": request.form.get("ip_dest"),
                "mac_addr": request.form.get("mac_addr"),
                "mac_dest": request.form.get("mac_dest"),
                "portSrc": request.form.get("portStart"),
                "portDst": request.form.get("portLimit"),
                "port_red_src": request.form.getlist("portRedSrc"),
                "port_red_dst": request.form.getlist("portRedDst"),
                "packet_protocol": request.form.get("packet_protocol"),
                # Datos Generales
                "general_ip": request.form.get("generalIp"),
                "general_port": request.form.get("generalPort"),
                "general_port_red": request.form.getlist("generalPortRed"),
                # Obtener los datos de comparadores
                "logic_operator_ip": request.form.get("logicOperatorIp"),
                "logic_operator_mac": request.form.get("logicOperatorMac"),
                "logic_operator_port": request.form.get("logicOperatorPort"),
                "logic_operator_protocol_red": request.form.get(
                    "logicOperatorProtoRed"
                ),
                "logic_operator_mac_port": request.form.get("logicOperatorMacPort"),
                "logic_operator_proto_red_proto": request.form.get(
                    "logicOperatorProtoRedProto"
                ),
            }
            return "Datos del formulario recibidos"

        elif request.method == "GET":
            try:

                ip_addr = form_data.get("ip_addr")
                ip_dest = form_data.get("ip_dest")
                mac_addr = form_data.get("mac_addr")
                mac_dest = form_data.get("mac_dest")
                port_red_src = form_data.get("port_red_src")
                port_red_dst = form_data.get("port_red_dst")
                portSrc = form_data.get("portSrc")
                portDst = form_data.get("portDst")
                packet_protocol = form_data.get("packet_protocol")
                # Datos generales
                general_ip = form_data.get("general_ip")
                general_port = form_data.get("general_port")
                general_port_red = form_data.get("general_port_red")
                # Comparadores
                logic_operator_ip = form_data.get("logic_operator_ip")
                logic_operator_mac = form_data.get("logic_operator_mac")
                logic_operator_port = form_data.get("logic_operator_port")
                logic_operator_protocol_red = form_data.get(
                    "logic_operator_protocol_red"
                )
                logic_operator_mac_port = form_data.get("logic_operator_mac_port")
                logic_operator_proto_red_proto = form_data.get(
                    "logic_operator_proto_red_proto"
                )

                return Response(
                    start_capture(
                        ip_addr,
                        ip_dest,
                        port_red_src,
                        port_red_dst,
                        portSrc,
                        portDst,
                        packet_protocol,
                        mac_addr,
                        mac_dest,
                        general_ip,
                        general_port,
                        general_port_red,
                        logic_operator_ip,
                        logic_operator_mac,
                        logic_operator_port,
                        logic_operator_protocol_red,
                        logic_operator_mac_port,
                        logic_operator_proto_red_proto,
                    ),
                    content_type="text/event-stream",
                )

            except Exception as e:
                # Manejar cualquier error que pueda ocurrir durante la captura
                return f"Error al capturar los paquetes: {e}"

    @app.route("/pre_start_capture", methods=["GET"])
    def pre_packet_capture():
        return Response(pre_start_capture(), content_type="text/event-stream")

    # Definir apertura de conexiones
    @app.route("/add_rule", methods=["POST"])
    @login_required
    def allow_rule():
        try:
            ip_addr = request.form.get("ip_addr")
            direction = request.form.get("fromto")
            netmask = request.form.get("netmask")
            ip_dest = request.form.get("ip_dest")
            dest_netmask = request.form.get("dest_netmask")
            port = request.form.get("port")
            portStart = request.form.get("portStart")
            portLimit = request.form.get("portLimit")
            protocol = request.form.get("protocol")
            entry = request.form.get("entry")
            comment = request.form.get("comment")

            response = allow_connections(
                ip_addr,
                port,
                protocol,
                entry,
                direction,
                netmask,
                ip_dest,
                dest_netmask,
                portStart,
                portLimit,
                comment,
            )
            return redirect(url_for("obtener_reglas_ufw_route"))
            # return render_template("config-firewall.html", response=response)
        except KeyError as e:
            return f"No se proporcionó el campo {e} en la solicitud POST."

    @app.route("/desactivar_regla", methods=["GET"])
    @login_required
    def desactivar_regla():
        try:
            contador = request.args.get("contador")
            numero = request.args.get("numero")
            nombre = request.args.get("nombre")
            fecha_creacion = request.args.get("fechaCreacion")
            ip = request.args.get("ip")
            accion = request.args.get("accion")
            protocolo = request.args.get("protocolo")
            entrada = request.args.get("entrada")
            direccion = request.args.get("direccion")

            regla_data = {
                "contador": contador,
                "numero": numero,
                "nombre": nombre,
                "fecha_creacion": fecha_creacion,
                "ip": ip,
                "accion": accion,
                "protocolo": protocolo,
                "entrada": entrada,
                "direccion": direccion,
            }

            regla_data_json = json.dumps(regla_data)

            deactivate_activate_rule(regla_data_json, numero, nombre)

            return redirect(url_for("obtener_reglas_ufw_route"))

        except Exception as e:
            # Maneja cualquier error que pueda ocurrir durante la desactivación
            return f"Error al desactivar la regla: {e}"

    # Eliminar una regla establecida
    @app.route("/eliminar_regla", methods=["GET"])
    @login_required
    def eliminar_regla():
        try:
            regla = request.args.get("regla")
            nombre = request.args.get("nombre")

            # Obtén el número de la regla utilizando el nuevo método
            response = delete_rule(regla, nombre)

            reglas = obtener_reglas_ufw()

            if "error" in reglas[0]:
                mensaje_error = reglas[0]["error"]
                return render_template("config-firewall.html", error=mensaje_error)

            # return render_template("config-firewall.html", reglas=reglas)
            return redirect(url_for("obtener_reglas_ufw_route"))

        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la eliminación
            return f"Error al eliminar la regla: {e}"
