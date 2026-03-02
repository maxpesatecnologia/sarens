from django.urls import path
from .views import receber_contato

urlpatterns = [
    path('enviar/', receber_contato, name='receber_contato'),
]