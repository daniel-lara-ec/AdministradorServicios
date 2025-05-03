from wakeonlan import send_magic_packet
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import paramiko
from ping3 import ping
import traceback
from onpremise_service.settings import (
    dict_servidores,
    SSH_KEY_NAME,
    CLAVE_API_AZURE,
    RUTA_API_CLOUD_VM,
)
import requests

key_path = f"/home/dmlaran/.ssh/{SSH_KEY_NAME}"
shutdown_command_linux = "sudo shutdown now"
shutdown_command_windows = "shutdown /s /f /t 0"


@login_required
def iniciar_servidor(request, servidor):

    validacion_encendido = ping(dict_servidores[servidor]["ip"], timeout=1)
    if validacion_encendido is None or validacion_encendido is False:

        try:

            # Envía el paquete mágico
            send_magic_packet(dict_servidores[servidor]["servidor"])

            messages.success(
                request,
                "Se ha enviado un paquete mágico al servidor con éxito.",
            )

            return redirect("panel")
        except Exception as e:
            messages.error(request, f"Error al enviar el paquete mágico: {str(e)}")

            return redirect("panel")

    else:
        messages.warning(
            request,
            "El servidor ya está encendido.",
        )
        return redirect("panel")


@login_required
def apagar_servidor(request, servidor):

    validacion_encendido = ping(dict_servidores[servidor]["ip"], timeout=1)
    if validacion_encendido is None or validacion_encendido is False:
        messages.warning(
            request,
            "El servidor ya está apagado.",
        )
        return redirect("panel")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        if dict_servidores[servidor]["tipo"] == "Windows":
            ssh_client.connect(
                dict_servidores[servidor]["ip"],
                username=dict_servidores[servidor]["usuario"],
                key_filename=key_path,
            )

            stdin, stdout, stderr = ssh_client.exec_command("shutdown /s /f /t 0\n")
            print(stdout.read().decode())
            print(stderr.read().decode())

            messages.success(
                request,
                "Se ha enviado el comando de apagado al servidor con éxito.",
            )

            return redirect("panel")

        elif dict_servidores[servidor]["tipo"] == "Linux":

            # Conectar al servidor remoto usando la clave privada
            ssh_client.connect(
                dict_servidores[servidor]["ip"],
                username=dict_servidores[servidor]["usuario"],
                key_filename=key_path,
            )

            # Ejecutar el comando de apagado
            stdin, stdout, stderr = ssh_client.exec_command(shutdown_command_linux)

            # Leer los errores, si los hay
            errors = stderr.read().decode()
            if errors:

                messages.error(
                    request,
                    f"Error al ejecutar el comando de apagado: {errors}",
                )
                return redirect("panel")
            else:
                messages.success(
                    request,
                    "Se ha enviado el comando de apagado al servidor con éxito.",
                )
                return redirect("panel")

    except Exception as e:
        messages.error(
            request,
            f"Error al conectar al servidor remoto: {str(e)}",
        )
        print(traceback.format_exc())
        return redirect("panel")

    finally:
        # Cierra la conexión SSH
        ssh_client.close()


@login_required
def iniciar_servidor_azure(request, servidor):

    DatosServidor = dict_servidores[servidor]
    NombreVM = DatosServidor["nombre_vm"]
    GrupoRecursos = DatosServidor["grupo_recursos"]

    respuesta = requests.get(
        f"{RUTA_API_CLOUD_VM}start?code={CLAVE_API_AZURE}&resource_group_name={GrupoRecursos}&vm_name={NombreVM}"
    )

    json_respuesta = respuesta.json()

    if json_respuesta["codigo"] == 200:
        messages.success(
            request,
            "Se ha enviado a Azure la solicitud de inicio al servidor con éxito.",
        )
        return redirect("panel")
    else:
        messages.error(
            request,
            f"Error al enviar la solicitud de inicio al servidor: {json_respuesta['Mensaje']}",
        )
        return redirect("panel")


@login_required
def apagar_servidor_azure(request, servidor):

    DatosServidor = dict_servidores[servidor]
    NombreVM = DatosServidor["nombre_vm"]
    GrupoRecursos = DatosServidor["grupo_recursos"]

    respuesta = requests.get(
        f"{RUTA_API_CLOUD_VM}stop?code={CLAVE_API_AZURE}&resource_group_name={GrupoRecursos}&vm_name={NombreVM}"
    )

    json_respuesta = respuesta.json()

    if json_respuesta["codigo"] == 200:
        messages.success(
            request,
            "Se ha enviado a Azure la solicitud de detención con éxito.",
        )
        return redirect("panel")
    else:
        messages.error(
            request,
            f"Error al enviar la solicitud de detención al servidor: {json_respuesta['Mensaje']}",
        )
        return redirect("panel")
