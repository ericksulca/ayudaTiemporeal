"""SistemaAyuda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from ayuda.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name="Home"),
    path('send/',nuevo,name="Send"),
    path('ayuda/getDatos/',getDatosAyuda,name='get_datosAyuda'),
    path('ayuda/nuevo/',AyudaCreateView.as_view(),name='ayuda_nuevo'),
    path('ayuda/persona-autocomplete/$',PersonaAutocomplete.as_view(),name='persona-autocomplete'),
    path('chat/<str:nombre>/', Room, name='room'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
