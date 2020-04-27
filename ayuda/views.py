
from django.contrib.auth import authenticate, login, logout
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
import json
import time
from ayuda.models import *
from ayuda.sendChat import *
from ayuda.forms.operacionForm import *

# Create your views here.
def Home(request):
	if request.method == 'GET':
		oOperaciones = Operacion.objects.filter(estado=1)
	
		return render(request, "home/index.html", {'oOperaciones':oOperaciones})

@csrf_exempt
def getDatosAyuda(request):
	if request.method == 'POST':
		dataPost = request.body
		Datos = json.loads(dataPost)
		print (Datos)
		jsonRespuesta = {}
		oOperacion = get_object_or_404(Operacion,pk=Datos["idOperacion"])
		oPersona = oOperacion.personas.all()[0]

		jsonRespuesta["exito"] = 1
		jsonRespuesta["fecha"]= str(oOperacion.fecha)
		jsonRespuesta["montoayuda"]=oOperacion.calcular_faltante()
		jsonRespuesta["idoperacion"]=oOperacion.id

		jsonRespuesta["nombre"]=oPersona.nombre
		jsonRespuesta["apellido"]=oPersona.apellido
		jsonRespuesta["descripcion"]=oPersona.descripcion
		jsonRespuesta["email"]=oPersona.email
		jsonRespuesta["telefono"]=oPersona.telefono
		jsonRespuesta["coordx"]=oPersona.coordx
		jsonRespuesta["coordy"]=oPersona.coordy
		jsonRespuesta["direccion"]=oPersona.direccion
		jsonRespuesta["imgpersona"]=oPersona.imgpersona.url
		jsonRespuesta["imghogar"]=oPersona.imghogar.url
		jsonRespuesta["tipooperacions"]=[]
		oTipooperacions = oPersona.tipooperacions.all()
		for oTipooperacion in oTipooperacions:
			jsonTipooperacion = {}
			jsonTipooperacion["id"] = oTipooperacion.id
			jsonTipooperacion["nombre"] = oTipooperacion.nombre
			jsonTipooperacion["imagen"] = oTipooperacion.imagen.url
			jsonTipooperacion["documento"] = oTipooperacion.documento.url
			jsonRespuesta["tipooperacions"].append(jsonTipooperacion)
		return HttpResponse(json.dumps(jsonRespuesta), content_type="application/json")

def nuevo(request):
	msgData = {}
	msgData["tipoMsg"]= 2
	msgData["message"]= "Nuevo Usuario conectado"
	Enviar_msg(request,msgData)
	return render(request, 'home/index2.html', {
			'room_name': 'home'
		})

def Room(request, room_name):
	return render(request, 'chat/room.html', {
		'room_name': room_name
	})
class AyudaCreateView(CreateView): # new
	model = Operacion
	form_class = OperacionForm
	template_name = 'ayuda/nuevo.html'
	def get(self, request, *args, **kwargs):
		if False == True:
			return HttpResponseRedirect(self.get_apertura_url())
		return render(request, self.template_name, {'form':self.form_class})

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.usuario = self.request.user
		obj.save()
		return HttpResponseRedirect(self.get_success_url(obj))

	def get_success_url(self,obj):
		return reverse('operacion_list', kwargs={})

	def get_apertura_url(self):
		return reverse('alumno_list', kwargs={})


class PersonaAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.is_authenticated():
			print ("no autenticado")
			return Persona.objects.none()

		qs = Persona.objects.filter(estado=1)
		if self.q:
			qs = qs.filter(nombre__istartswith=self.q)
			print(qs)

		print ("ingresó metodo")
		return self.q

