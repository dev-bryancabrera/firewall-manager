from datetime import datetime
import json
import shlex
from flask import flash
from flask_login import current_user, login_user

# import pymysql
import re

import subprocess

# Models
from models.modelUser import modelUser
from models.modelFirewall import modelFirewall
from models.modelMonitoreo import modelPaquetes

# Entities
from models.entities.user import User
from models.entities.rules import Firewall
from models.entities.monitoreo import Monitoreo


# Función para realizar una consulta a la base de datos
def validar_ingreso(username, password_hash):
    try:
        user = User(0, username, password_hash)
        logged_user = modelUser.login(user)
        if logged_user != None:
            if logged_user.password_hash:
                login_user(logged_user)
                return True
            else:
                flash("Credenciales Erroneas")
                return False
        else:
            flash("Usuario no Encontrado")
            return False
    except Exception as e:
        return str(e)


numero = 0


def obtener_reglas_ufw():
    try:
        salida = subprocess.check_output(["sudo", "ufw", "status", "numbered"])
        reglas = salida.decode("utf-8").splitlines()

        # Filtrar las líneas que comienzan con '[', eliminar "(out)" y ajustar los espacios en los números
        consulta_formateada = "\n".join(
            [
                re.sub(r"\(out\)", "", re.sub(r"\[\s*(\d+)\]", r"[\1]", line.strip()))
                for line in reglas
                if line.startswith("[")
            ]
        )

        # Almacenar las reglas
        reglas_in = []
        reglas_out = []
        data_lista = []

        contador_entrada = 0
        contador_salida = 0
        contador_verificar = 0
        count_data = 0

        global numero

        deactivate_rules = modelFirewall.getRulesDeactivate()
        for row in deactivate_rules:
            deactivate_data = row[1]
            data = json.loads(deactivate_data)

            status_data = row[2]

            contador_data = data["contador"]
            numero_data = data["numero"]
            nombre_data = data["nombre"]
            fecha_creacion_data = data["fecha_creacion"]
            ip_data = data["ip"]
            accion_data = data["accion"]
            protocolo_data = data["protocolo"]
            entrada_data = data["entrada"]
            direccion_data = data["direccion"]
            estado_data = status_data
            contador_data_format = int(contador_data)
            data_lista.append(
                (
                    contador_data_format,
                    numero_data,
                    nombre_data,
                    fecha_creacion_data,
                    ip_data,
                    accion_data,
                    protocolo_data,
                    entrada_data,
                    direccion_data,
                    estado_data,
                )
            )

        # Dividir la consulta formateada en líneas
        for line in consulta_formateada.split("\n"):
            # Ignorar las líneas vacías
            if line:
                contador_verificar += 1
                # Dividir la cadena en dos partes: antes y después del #
                parts_before_comment = re.split(r"\s+#", line, maxsplit=1)
                # Separar las partes antes del comentario utilizando la expresión regular original
                parts = re.split(r"\s+|(?<=\S)/(?=\S)", parts_before_comment[0])
                # Unir las partes antes del comentario con el comentario (si existe)
                # Definir la variable para el comentario (si existe)
                nombre = (
                    parts_before_comment[1].lstrip()
                    if len(parts_before_comment) > 1
                    else None
                )

                created_date = ""
                status = 1
                rule_db = modelFirewall.getRuleByName(nombre)
                if rule_db:
                    created_date = rule_db[5].strftime("%Y-%m-%d")
                    status = rule_db[6]

                while True:
                    # Verificar si el contador está en data_lista
                    if contador_verificar in [item[0] for item in data_lista]:
                        for item in data_lista:
                            if item[0] == contador_verificar and item[7] == "ENTRADA":
                                
                                count_data += 1
                                # Asignar los valores de la tupla a regla
                                regla = {
                                    "contador": item[0],
                                    "numero": item[1],
                                    "nombre": item[2],
                                    "fecha_creacion": item[3],
                                    "ip": item[4],
                                    "accion": item[5],
                                    "protocolo": item[6],
                                    "entrada": item[7],
                                    "direccion": item[8],
                                    "estado": item[9],
                                }

                                reglas_in.append(regla)

                                contador_verificar += 1
                                contador_entrada += 1
                                # Salir del bucle ya que encontramos la tupla correspondiente
                                #break
                            if item[0] == contador_verificar and item[7] == "SALIDA":
                                
                                count_data += 1
                                # Asignar los valores de la tupla a regla
                                regla = {
                                    "contador": item[0],
                                    "numero": item[1],
                                    "nombre": item[2],
                                    "fecha_creacion": item[3],
                                    "ip": item[4],
                                    "accion": item[5],
                                    "protocolo": item[6],
                                    "entrada": item[7],
                                    "direccion": item[8],
                                    "estado": item[9],
                                }

                                reglas_out.append(regla)

                                contador_verificar += 1
                                contador_salida += 1
                                # Salir del bucle ya que encontramos la tupla correspondiente
                                #break

                    else:
                        break

                print(contador_verificar)

                # Eliminar elementos vacíos y corchetes del número inicial
                parts = [re.sub(r"\[|\]", "", part) for part in parts if part]

                # Verificar un mínimo de elementos
                if len(parts) >= 4:
                    # Obtener los valores específicos
                    numero = parts[0]

                    # Verificar y asignar los valores
                    direccion = (
                        parts[1] + ":" + parts[2]
                        if parts[1] not in ["tcp", "udp", "(v6)"]
                        and parts[2]
                        not in ["IN", "OUT", "ALLOW", "DENY", "tcp", "udp", "(v6)"]
                        else (
                            parts[1] if parts[1] not in ["tcp", "udp", "(v6)"] else ""
                        )
                    )

                    netmask = (
                        parts[1] + ":" + parts[2]
                        if parts[1] not in ["tcp", "udp", "(v6)"]
                        and parts[2]
                        not in ["IN", "OUT", "ALLOW", "DENY", "tcp", "udp", "(v6)"]
                        else (
                            parts[1] if parts[1] not in ["tcp", "udp", "(v6)"] else ""
                        )
                    )

                    # Buscar desde la posición 2 en adelante si contiene (v6) y concatenar si es necesario
                    for i in range(2, len(parts)):
                        if parts[i] == "(v6)":
                            direccion += parts[i]
                            break

                    # Buscar en todas las posiciones en caso de que accion y entrada estén vacías
                    accion = next((p for p in parts[2:] if p in ["DENY", "ALLOW"]), "")
                    entrada = next((p for p in parts[3:] if p in ["IN", "OUT"]), "")

                    # Buscar en todas las posiciones si no se encuentra en las posiciones específicas
                    protocolo = next(
                        (p for p in parts if p in ["tcp", "udp"]), "tcp/udp"
                    )

                    ip_parts = []

                    # Verificar si parts[4] no está en la lista de valores prohibidos
                    if len(parts) >= 5 and parts[4] not in [
                        "tcp",
                        "udp",
                        "(v6)",
                        "DENY",
                        "ALLOW",
                        "IN",
                        "OUT",
                    ]:
                        ip_parts.append(
                            parts[4]
                        )  # Agregar parts[4] a ip_parts si cumple con la condición

                    # Agregar los elementos restantes de parts a ip_parts, excluyendo los valores prohibidos
                    ip_parts.extend(
                        p
                        for p in parts[5:]
                        if p not in ["tcp", "udp", "(v6)", "DENY", "ALLOW", "IN", "OUT"]
                    )

                    # Unir los elementos de ip_parts con ":" como delimitador para formar la dirección IP
                    ip = ":".join(ip_parts)

                    for i in range(4, len(parts)):
                        if parts[i] == "(v6)":
                            ip += parts[i]
                            break

                    # Cambiar a espa;ol
                    if accion == "ALLOW":
                        permiso = "PERMITIDO"
                    elif accion == "ALLOW":
                        permiso = "DENEGADO"

                    if entrada == "IN":
                        contador_entrada += 1
                        contador = contador_entrada
                        entry = "ENTRADA"
                    elif entrada == "OUT":
                        contador_salida += 1
                        contador = contador_salida
                        entry = "SALIDA"

                    # Crear un diccionario con los valores
                    regla = {
                        "contador": contador,
                        "numero": numero,
                        "nombre": nombre,
                        "fecha_creacion": created_date,
                        "direccion": direccion,
                        "accion": permiso,
                        "protocolo": (
                            protocolo.upper()
                            if protocolo in ["tcp", "udp"]
                            else "TCP/UDP"
                        ),
                        "entrada": entry,
                        "ip": ip,
                        "estado": status,
                    }

                    # Agregar el diccionario a la lista correspondiente (IN o OUT)
                    if entrada == "IN":
                        reglas_in.append(regla)
                    elif entrada == "OUT":
                        reglas_out.append(regla)

        contador_maximo = len(deactivate_rules)
        while True:
            if count_data <= contador_maximo:
                contador_verificar += 1
                if contador_verificar in [item[0] for item in data_lista]:
                    print("here")
                    for item in data_lista:
                        if item[0] == contador_verificar:
                            # Asignar los valores de la tupla a regla
                            regla = {
                                "contador": item[0],
                                "numero": item[1],
                                "nombre": item[2],
                                "fecha_creacion": item[3],
                                "ip": item[4],
                                "accion": item[5],
                                "protocolo": item[6],
                                "entrada": item[7],
                                "direccion": item[8],
                                "estado": item[9],
                            }
                            # Salir del bucle ya que encontramos la tupla correspondiente
                            break

                    if item[7] == "ENTRADA":
                        reglas_in.append(regla)
                    elif item[7] == "SALIDA":
                        reglas_out.append(regla)

                else:
                    count_data += 1
            else:
                break

        return reglas_in, reglas_out
    except subprocess.CalledProcessError as e:
        return [{"error": f"Error al obtener reglas UFW: {e}"}]


def scan_network():
    try:
        # Comando arp-scan para escanear la red
        command = "sudo arp-scan -l"
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        # Decodificar la salida del comando arp-scan de bytes a texto
        output = stdout.decode()

        ips = []
        macs = []
        devices = []

        pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

        for line in output.split("\n"):
            if line.strip() and pattern.match(line.split()[0]):
                parts = line.split()
                ip = parts[0]
                mac = parts[1]

                device = {
                    "ip": ip,
                    "mac": mac,
                }
                devices.append(device)

        return devices

    except Exception as e:
        return [{"error": f"Error al procesar la línea: {line}, {e}"}]


def start_capture(
    ip_addr,
    ip_dest,
    port_red_src,
    port_red_dst,
    port_src,
    port_dst,
    packet_protocol,
    mac_addr,
    mac_dest,
    generalIp,
    generalPort,
    generalPortRed,
    logic_operator_ip,
    logic_operator_mac,
    logic_operator_port,
    logic_operator_protocol_red,
    logic_operator_mac_port,
    logic_operator_proto_red_proto,
):

    patron_coma = re.compile(r",\s*")

    # Variables Custom
    ips_custom = ""
    port_custom = ""
    protocol_custom = ""
    command_filter = ""

    # Manejo de ips
    if ip_addr:
        if patron_coma.search(ip_addr):
            src_ips = patron_coma.sub(" or ", ip_addr)
            src_host = f"src host {src_ips}"
        else:
            src_host = f"src host {ip_addr}"

    if ip_dest:
        if patron_coma.search(ip_dest):
            dst_ips = patron_coma.sub(" or ", ip_dest)
            dst_host = f"dst host {dst_ips}"
        else:
            dst_host = f"dst host {ip_dest}"

    if generalIp:
        if patron_coma.search(generalIp):
            general_ips = patron_coma.sub(" or ", generalIp)
            general_host = f"host {general_ips}"
        else:
            general_host = f"host {generalIp}"

    # Manejo de MACS
    if mac_addr:
        if patron_coma.search(mac_addr):
            src_macs = patron_coma.sub(" or ", mac_addr)
            src_ether = f"ether src {src_macs}"
        else:
            src_ether = f"ether src {mac_addr}"

    if mac_dest:
        if patron_coma.search(mac_dest):
            dst_macs = patron_coma.sub(" or ", mac_dest)
            dst_ether = f"ether dst {dst_macs}"
        else:
            dst_ether = f"ether dst {mac_dest}"

    if ip_addr and ip_dest and mac_addr and mac_dest:
        ips_custom = f"({src_host} {logic_operator_ip} {dst_host} or {src_ether} {logic_operator_mac} {dst_ether})"
    elif ip_addr and ip_dest and mac_addr:
        ips_custom = f"({src_host} {logic_operator_ip} {dst_host} or {src_ether})"
    elif ip_addr and ip_dest and mac_dest:
        ips_custom = f"({src_host} {logic_operator_ip} {dst_host} or {dst_ether})"
    elif mac_addr and mac_dest and generalIp:
        ips_custom = f"({src_ether} {logic_operator_mac} {dst_ether} or {general_host})"
    elif mac_addr and mac_dest and ip_addr:
        ips_custom = f"({src_ether} {logic_operator_mac} {dst_ether} or {src_host})"
    elif mac_addr and mac_dest and ip_dest:
        ips_custom = f"({src_ether} {logic_operator_mac} {dst_ether} or {dst_host})"
    elif ip_addr and mac_addr:
        ips_custom = f"({src_host} or {src_macs})"
    elif ip_addr and mac_dest:
        ips_custom = f"({src_host} or {dst_macs})"
    elif ip_dest and mac_addr:
        ips_custom = f"({dst_host} or {src_macs})"
    elif ip_dest and mac_dest:
        ips_custom = f"({dst_host} or {dst_macs})"
    elif mac_addr and generalIp:
        ips_custom = f"({src_ether} or {general_host})"
    elif mac_dest and generalIp:
        ips_custom = f"({dst_ether} or {general_host})"
    elif ip_addr and ip_dest:
        ips_custom = f"({src_host} {logic_operator_ip} {dst_host})"
    elif ip_addr:
        ips_custom = f"({src_host})"
    elif ip_dest:
        ips_custom = f"({dst_host})"
    elif generalIp:
        ips_custom = f"({general_host})"
    elif mac_addr and mac_dest:
        ips_custom = f"({src_ether} {logic_operator_mac} {dst_ether})"
    elif mac_addr:
        ips_custom = f"({src_ether})"
    elif mac_dest:
        ips_custom = f"({dst_ether})"

    # Manejo de Puertos
    if port_src:
        if patron_coma.search(port_src):
            src_ports = patron_coma.sub(" or ", port_src)
            src_port = f"src port {src_ports}"
        else:
            src_port = f"src port {port_src}"

    if port_dst:
        if patron_coma.search(port_dst):
            dst_ports = patron_coma.sub(" or ", port_dst)
            dst_port = f"dst port {dst_ports}"
        else:
            dst_port = f"dst port {port_dst}"

    if generalPort:
        if patron_coma.search(generalPort):
            general_ports = patron_coma.sub(" or ", generalPort)
            general_port = f"port {general_ports}"
        else:
            general_port = f"port {generalPort}"

    if port_red_src:
        combined_port_red_src = " or ".join(port_red_src)
        src_port_red = f"src port {combined_port_red_src}"

    if port_red_dst:
        combined_port_red_dst = " or ".join(port_red_dst)
        dst_port_red = f"dst port {combined_port_red_dst}"

    if generalPortRed:
        combined_port_red_general = " or ".join(generalPortRed)
        general_port_red = f"port {combined_port_red_general}"

    # Puertos
    if port_src and port_dst and port_red_src and port_red_dst:
        port_custom = f"({src_port} {logic_operator_port} {dst_port} or {src_port_red} {logic_operator_protocol_red} {port_red_dst})"
    elif port_src and port_dst and port_red_src:
        port_custom = f"({src_port} {logic_operator_port} {dst_port} or {src_port_red})"
    elif port_src and port_dst and port_red_dst:
        port_custom = f"({src_port} {logic_operator_port} {dst_port} or {port_red_dst})"
    elif port_red_src and port_red_dst and port_src:
        port_custom = f"({src_port_red} {logic_operator_protocol_red} {port_red_dst} or {src_port})"
    elif port_red_src and port_red_dst and port_dst:
        port_custom = f"({src_port_red} {logic_operator_protocol_red} {port_red_dst} or {dst_port})"
    elif port_src and port_dst and generalPortRed:
        port_custom = (
            f"({src_port} {logic_operator_port} {dst_port} or port {general_port_red})"
        )
    elif port_red_src and port_red_dst and generalPort:
        port_custom = f"({src_port_red} {logic_operator_protocol_red} {port_red_dst} or port {general_port})"
    # Doble dato
    elif generalPortRed and generalPort:
        port_custom = f"(port {general_port} or port {general_port_red})"
    elif port_src and generalPortRed:
        port_custom = f"({src_port} or port {general_port_red})"
    elif port_dst and generalPortRed:
        port_custom = f"({src_port} or port {general_port_red})"
    elif port_red_src and generalPort:
        port_custom = f"({src_port_red} or port {general_port})"
    elif port_red_dst and generalPort:
        port_custom = f"({src_port_red} or port {general_port})"
    elif port_src and port_dst:
        port_custom = f"({src_port} {logic_operator_port} {dst_port})"
    elif port_red_src and port_red_dst:
        port_custom = f"({src_port_red} {logic_operator_protocol_red} {port_red_dst})"
    elif port_red_src and port_src:
        port_custom = f"({src_port_red} or {src_port})"
    elif port_red_src and port_dst:
        port_custom = f"({src_port_red} or {dst_port})"
    elif port_src and port_red_dst:
        port_custom = f"({dst_port_red} or {src_port})"
    elif port_red_dst and port_dst:
        port_custom = f"({dst_port_red} or {dst_port})"
    elif port_src:
        port_custom = f"({src_port})"
    elif port_dst:
        port_custom = f"({dst_host})"
    elif generalPort:
        port_custom = f"(port {general_port})"
    elif port_red_src:
        port_custom = f"({src_port_red})"
    elif port_red_dst:
        port_custom = f"({dst_port_red})"
    elif generalPortRed:
        port_custom = f"(port {general_port_red})"

    # Manejo de protocolos  ||  Siempre debe ir al final
    if packet_protocol == "tcp":
        protocol_custom = f"(tcp)"
    elif packet_protocol == "udp":
        protocol_custom = f"(udp)"
    elif packet_protocol == "tcp/udp":
        protocol_custom = f"(tcp or udp)"

    # Unir elementos para formar el filtro
    if ips_custom and port_custom and protocol_custom:
        command_filter = f"{ips_custom} {logic_operator_mac_port} {port_custom} {logic_operator_proto_red_proto} {protocol_custom}"
    elif ips_custom and port_custom:
        command_filter = f"{ips_custom} {logic_operator_mac_port} {port_custom}"
    elif ips_custom and protocol_custom:
        command_filter = f"{ips_custom} {logic_operator_mac_port} {protocol_custom}"
    elif port_custom and protocol_custom:
        command_filter = (
            f"{port_custom} {logic_operator_proto_red_proto} {protocol_custom}"
        )
    elif ips_custom:
        command_filter = f"{ips_custom}"
    elif port_custom:
        command_filter = f"{port_custom}"
    elif protocol_custom:
        command_filter = f"{protocol_custom}"

    # print(command_filter)
    if command_filter == "":
        custom_command = (
            f"(tcp or udp) and (port http or https or smtp or ssh or ftp or telnet)"
        )
    else:
        custom_command = command_filter

    base_command = [
        "sudo",
        "tcpdump",
        # "-n"   # Muestra el trafico los host en formato de ip y no de dominio
        "-l",
        "-c",
        "100",
        "-i",
        "eth0",  # Hay que sacar la info de la interfaz de red donde se instale el sistema
    ]

    # Valores personalizados que pueden concatenarse
    custom_values = [
        custom_command,
    ]

    end_command = [
        "-tttt",
        "-q",
        "-v",
    ]

    # Concatenar las dos partes del comando
    command = base_command + custom_values + end_command

    print("filtro creado >", command_filter)
    print("Comando > ", command)

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    )

    for line in process.stdout:

        if "ARP" in line:
            arp_info = line.strip().split(",")
            arp_parts = arp_info[0].split(" ")
            time = " ".join(arp_parts[:2])
            time_formatted = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            src_ip_domain = ""
            src_port = ""
            dst_ip_domain = ""
            dst_port = ""
            protocol = ""
            info = " ".join(arp_info[2:])
            yield f"data: {time_formatted} {src_ip_domain}:{src_port} > {dst_ip_domain}:{dst_port} {protocol} {info}\n\n"
        else:
            line2 = process.stdout.readline().strip()

            if not line2:
                break

            combined_line = line.strip() + " " + line2.strip()

        parts = []
        parenthesis_count = 0
        current_part = ""

        for char in combined_line:

            if char == "(":
                parenthesis_count += 1
            elif char == ")":
                parenthesis_count -= 1

            if parenthesis_count > 0:
                current_part += char
            else:
                if char == " " and current_part:
                    parts.append(current_part)
                    current_part = ""
                else:
                    current_part += char

        if current_part:
            parts.append(current_part)

        if len(parts) >= 6:
            time = " ".join(parts[:2])
            time_formatted = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            info = parts[3]

            info_parts = parts[3].rsplit(",", 6)
            info_protocol = info_parts[5].rsplit(" ", 2)
            protocol = info_protocol[1]

            src_parts = parts[4].rsplit(".", 1)
            src_ip_domain = src_parts[0]
            src_port = src_parts[1] if len(src_parts) > 1 else None

            dst_parts = parts[6].rsplit(".", 1)
            dst_ip_domain = dst_parts[0]
            dst_port = dst_parts[1].rstrip(":") if len(dst_parts) > 1 else None

            yield f"data: {time_formatted} {src_ip_domain}:{src_port} > {dst_ip_domain}:{dst_port} {protocol} {info}\n\n"


def pre_start_capture():

    custom_command = (
        f"(tcp or udp) and (port http or https or smtp or ssh or ftp or telnet)"
    )

    base_command = [
        "sudo",
        "tcpdump",
        # "-n"   # Muestra el trafico los host en formato de ip y no de dominio
        "-l",
        "-c",
        "100",
        "-i",
        "eth0",  # Hay que sacar la info de la interfaz de red donde se instale el sistema
    ]

    # Valores personalizados que pueden concatenarse
    custom_values = [
        custom_command,
    ]

    end_command = [
        "-tttt",
        "-q",
        "-v",
    ]

    # Concatenar las dos partes del comando
    command = base_command + custom_values + end_command

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    )

    for line in process.stdout:

        if "ARP" in line:
            arp_info = line.strip().split(",")
            arp_parts = arp_info[0].split(" ")
            time = " ".join(arp_parts[:2])
            time_formatted = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            src_ip_domain = ""
            src_port = ""
            dst_ip_domain = ""
            dst_port = ""
            protocol = ""
            info = " ".join(arp_info[2:])
            yield f"data: {time_formatted} {src_ip_domain}:{src_port} > {dst_ip_domain}:{dst_port} {protocol} {info}\n\n"
        else:
            line2 = process.stdout.readline().strip()

            if not line2:
                break

            combined_line = line.strip() + " " + line2.strip()

        parts = []
        parenthesis_count = 0
        current_part = ""

        for char in combined_line:

            if char == "(":
                parenthesis_count += 1
            elif char == ")":
                parenthesis_count -= 1

            if parenthesis_count > 0:
                current_part += char
            else:
                if char == " " and current_part:
                    parts.append(current_part)
                    current_part = ""
                else:
                    current_part += char

        if current_part:
            parts.append(current_part)

        if len(parts) >= 6:
            time = " ".join(parts[:2])
            time_formatted = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            info = parts[3]

            info_parts = parts[3].rsplit(",", 6)
            info_protocol = info_parts[5].rsplit(" ", 2)
            protocol = info_protocol[1]

            src_parts = parts[4].rsplit(".", 1)
            src_ip_domain = src_parts[0]
            src_port = src_parts[1] if len(src_parts) > 1 else None

            dst_parts = parts[6].rsplit(".", 1)
            dst_ip_domain = dst_parts[0]
            dst_port = dst_parts[1].rstrip(":") if len(dst_parts) > 1 else None

            yield f"data: {time_formatted} {src_ip_domain}:{src_port} > {dst_ip_domain}:{dst_port} {protocol} {info}\n\n"


# Obtener el numero de la regla
def delete_rule(regla, nombre):
    try:

        # Ejecuta el comando ufw status numbered y captura la salida
        subprocess.run(["sudo", "ufw", "delete", regla], input="y\n", text=True)

        if nombre:
            modelFirewall.deleteRule(nombre)

        return f"Regla Numero {regla} Eliminada"
    except subprocess.CalledProcessError as e:
        # Maneja cualquier error que pueda ocurrir durante la ejecución del comando
        print(f"Error al obtener el número de la regla: {e}")
        return None


def deactivate_activate_rule(regla, numero_regla, nombre):
    try:

        if nombre:
            rule_db = modelFirewall.getRuleByName(nombre)
            if rule_db:
                numero_data = int(rule_db[6])
                if numero_data == 1:
                    subprocess.run(
                        ["sudo", "ufw", "delete", numero_regla], input="y\n", text=True
                    )
                    modelFirewall.updateRule(0, regla, nombre)
                    return f"Regla Numero {regla} Eliminada"
                elif numero_data == 0:
                    print(numero)
                    rule_data = json.loads(rule_db[3])
                    numero_data = rule_data.get("numero", "")
                    comment = rule_db[2]

                    if numero < numero_data:
                        rule = f"sudo ufw {rule_db[7]} comment '{comment}'"
                    else:
                        rule = f"sudo ufw insert {numero_data} {rule_db[7]} comment '{comment}'"

                    print(rule)
                    subprocess.run(shlex.split(f"{rule}"))

                    modelFirewall.updateRule(1, None, nombre)
                    return f"Regla Numero {numero_data} Creada"
            else:
                return f"No se encontró una regla con el nombre {nombre}"

        return f"El nombre de la regla no puede ser None o vacío"
    except subprocess.CalledProcessError as e:
        # Maneja cualquier error que pueda ocurrir durante la ejecución del comando
        print(f"Error al obtener el número de la regla: {e}")
        return None


def allow_connections(
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
):

    try:

        ip_dest = "any"

        if entry == "in":
            direction = "from"
        elif entry == "out":
            direction = "to"
            ip_dest = ""

        rule = "sudo ufw allow"

        if (port or portStart or portLimit) and ip_addr:

            if ip_addr and netmask:
                ip_addr += f"/{netmask}"
            if ip_dest and dest_netmask:
                ip_dest += f"/{dest_netmask}"

            if entry and direction and ip_addr and portStart and portLimit and protocol:
                rule += f" {entry} {direction} {ip_addr} port {portStart}:{portLimit} proto {protocol}"
                rule += f" comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif (
                entry
                and direction
                and ip_addr
                and portStart
                and ip_dest
                and portLimit
                and protocol
            ):
                rule += f" {entry} {direction} {ip_addr} port {portStart} to {ip_dest} port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif (
                entry and direction and ip_addr and portStart and ip_dest and portLimit
            ):
                rule += f" {entry} {direction} {ip_addr} port {portStart} to {ip_dest} port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and ip_dest and port and protocol:
                rule += f" {entry} {direction} {ip_addr} to {ip_dest} port {port} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif (
                entry and direction and ip_addr and portStart and portLimit and protocol
            ):
                rule += f" {entry} {direction} {ip_addr} port {portStart} to any port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif (
                entry and direction and portStart and ip_dest and portLimit and protocol
            ):
                rule += f" {entry} {direction} any port {portStart} to {ip_dest} port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and portStart and ip_dest and portLimit:
                rule += f" {entry} {direction} any port {portStart} to {ip_dest} port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart and portLimit:
                rule += f" {entry} {direction} {ip_addr} port {portStart} to any port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            # Otras
            elif entry and direction and ip_addr and portLimit and protocol:
                rule += f" {entry} {direction} {ip_addr} to any port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart and ip_dest and protocol:
                rule += f" {entry} {direction} {ip_addr} port {portStart} to {ip_dest} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart and protocol:
                rule += f" {entry} {direction} {ip_addr} port {portStart} to any proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif (
                entry and direction and ip_dest and portStart and portLimit and protocol
            ):
                rule += f" {entry} {direction} any port {portStart} to {ip_dest} port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest and portLimit and protocol:
                rule += f" {entry} {direction} any to {ip_dest} port {portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and portStart and ip_dest and portLimit:
                rule += f" {entry} {direction} any port {portStart} to {ip_dest} port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart and ip_dest:
                rule += f" {entry} {direction} {ip_addr} port {portStart} to {ip_dest} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart:
                rule += f" {entry} {direction} {ip_addr} port {portStart} to any comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portLimit:
                rule += f" {entry} {direction} {ip_addr} to any port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest and portLimit:
                rule += f" {entry} {direction} any to {ip_dest} port {portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            # Otro
            elif entry and direction and ip_addr and port and protocol:
                rule += f" {entry} {direction} {ip_addr} port {port} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and portStart and portLimit:
                rule += f" {entry} {direction} {ip_addr} port {portStart}:{portLimit} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and ip_dest and port:
                rule += f" {entry} {direction} {ip_addr} to {ip_dest} port {port} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and ip_dest and port:
                rule += f" {entry} {direction} {ip_addr} to {ip_dest} {port} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest and port and protocol:
                rule += f" {entry} {direction} any to {ip_dest} port {port} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            # elif entry and direction and ip_addr and port and protocol:
            #    rule += f" {entry} {direction} {ip_addr} to any port {port} proto {protocol}"
            #    rule += f" comment '{comment}'"
            #    subprocess.run(shlex.split(f'{rule}'))
            #

            # elif entry and direction and ip_addr and port:
            #    rule += f" {entry} {direction} {ip_addr} to any port {port}"
            #    rule += f" comment '{comment}'"
            #    subprocess.run(shlex.split(f'{rule}'))
            #

            elif entry and direction and ip_addr and port and protocol:
                rule += f" {entry} {direction} {ip_addr} port {port} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and port:
                rule += (
                    f" {entry} {direction} {ip_addr} port {port} comment '{comment}'"
                )
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest and port:
                rule += f" {entry} {direction} any to {ip_dest} port {port} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

        # IPs
        elif ip_addr:

            if ip_addr and netmask:
                ip_addr += f"/{netmask}"
            if ip_dest and dest_netmask:
                ip_dest += f"/{dest_netmask}"

            if entry and direction and ip_addr and ip_dest and protocol:
                rule += f" {entry} {direction} {ip_addr} to {ip_dest} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and protocol:
                rule += f" {entry} {direction} {ip_addr} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest and protocol:
                rule += f" {entry} {direction} any to {ip_dest} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr and ip_dest:
                rule += (
                    f" {entry} {direction} {ip_addr} to {ip_dest} comment '{comment}'"
                )
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_addr:
                rule += f" {entry} {direction} {ip_addr} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and ip_dest:
                rule += f" {entry} {direction} any to {ip_dest} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

        # Port
        elif port or portStart or portLimit:

            if entry and direction and portStart and portLimit and protocol:
                rule += f" {entry} {direction} any port {portStart}:{portLimit} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            # De ver
            # elif entry and portStart and portLimit and protocol:
            #    rule += f" {entry} from any port {portStart} to any port {portLimit} proto {protocol}"
            #    rule += f" comment '{comment}'"
            #    subprocess.run(shlex.split(f'{rule}'))
            #

            # elif entry and portStart and portLimit:
            #    rule += f" {entry} from any port {portStart} to any port {portLimit}"
            #    rule += f" comment '{comment}'"
            #    subprocess.run(shlex.split(f'{rule}'))
            #
            # De ver

            elif entry and direction and port and protocol:
                rule += f" {entry} {direction} any port {port} proto {protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and portStart and portLimit and protocol:
                rule += (
                    f" {entry} {portStart}:{portLimit}/{protocol} comment '{comment}'"
                )
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and port and protocol:
                rule += f" {entry} {port}/{protocol} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and direction and port:
                rule += f" {entry} {direction} any port {port} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

            elif entry and port:
                rule += f" {entry} {port} comment '{comment}'"
                subprocess.run(shlex.split(f"{rule}"))

        rule_format = rule.replace("sudo ufw ", "")

        # Encontrar el índice del comentario y eliminarlo
        indice_comentario = rule_format.find("comment")
        if indice_comentario != -1:
            rule_save = rule_format[:indice_comentario].strip()
        else:
            rule_save = rule_format
        print(rule_save)
        fecha_creacion = datetime.now()
        firewall = Firewall(
            0, comment, None, "por ver", rule_save, fecha_creacion, 1, current_user.id
        )
        modelFirewall.insertRule(firewall)

        return f"Regla creada {rule}"
    except subprocess.CalledProcessError:
        return "Error al permitir el puerto."
