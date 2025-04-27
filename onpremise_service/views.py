from django.shortcuts import render
from django.http import JsonResponse
from wakeonlan import send_magic_packet
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def panel(request):
    return render(request, "panel.html")


@login_required
def IniciarSesion(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o contraseña incorrectos",
                },
            )

        else:
            login(request, user)
            return redirect("panel")


@login_required
def CerrarSesion(request):
    logout(request)
    return redirect("login")
