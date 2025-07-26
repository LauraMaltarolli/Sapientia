"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('dilemas/', DilemaListView.as_view(), name='dilema_list'),
    path('dilemas/<int:pk>/', DilemaDetailView.as_view(), name='dilema_detail'),
    path('meu-diario/', DiarioView.as_view(), name='diario'),
    path('contas/cadastro/', CadastroView.as_view(), name='cadastro'),
    path('contas/', include('django.contrib.auth.urls')),
    path('teste/', TesteFilosoficoView.as_view(), name='teste'),
    path('teorias/', TeoriaFilosoficaListView.as_view(), name='teoria_list'),
    path('teorias/<int:pk>/', TeoriaFilosoficaDetailView.as_view(), name='teoria_detail'),
    path('dilemas/criar/', DilemaCreateView.as_view(), name='dilema_create'),
]
