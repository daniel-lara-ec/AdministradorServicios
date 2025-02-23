from django.urls import path

from . import views

urlpatterns = [
    path(
        "iniciar_servidor/<str:servidor>",
        views.iniciar_servidor,
        name="inciar_servidor",
    ),
    path(
        "apagar_servidor/<str:servidor>",
        views.apagar_servidor,
        name="apagar_servidor",
    ),
    path(
        "iniciar_servidor_azure/<str:servidor>",
        views.iniciar_servidor_azure,
        name="iniciar_servidor_azure",
    ),
    path(
        "apagar_servidor_azure/<str:servidor>",
        views.apagar_servidor_azure,
        name="apagar_servidor_azure",
    ),
]
