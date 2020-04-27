from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from ayuda.sendChat import *

class Item(models.Model):
	nombre   = models.CharField(verbose_name=u"Nombre",max_length=45)
	html     = models.TextField(verbose_name=u"HTML",blank=True,null=True)
	def __str__(self):
		return self.nombre

class Requisito(models.Model):
	nombre  = models.CharField(verbose_name=u"Nombre",max_length=45)
	item = models.ForeignKey(Item, related_name='item_requisitos',on_delete=models.CASCADE,blank=True,null=True)
	def __str__(self):
		return self.nombre

class Tipooperacion(models.Model):
	nombre     = models.CharField(verbose_name=u"Nombre",max_length=45)
	imagen     = models.ImageField(verbose_name=u"Imagen tipo de operación",blank=True, null=True,default="no-img-TOP.png",upload_to='imgTipoOperacion')#upload_to='%Y/%m/%d',
	documento  = models.FileField(verbose_name=u"Documento tipo de operación",blank=True, null=True,upload_to='docTipoOperacion')#upload_to='%Y/%m/%d',
	requisitos = models.ManyToManyField(Requisito)
	def __str__(self):
		return self.nombre

class Persona(models.Model):
	usuario      = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
	tipousuario  = models.IntegerField(default=1)
	nombre       = models.CharField(verbose_name=u"Nombres",max_length=45)
	apellido     = models.CharField(verbose_name=u"Apellidos",max_length=45)
	email	     = models.CharField(verbose_name=u"E-Mail",max_length=45)
	telefono     = models.CharField(verbose_name=u"Teléfono",max_length=12)
	coordx		 = models.CharField(verbose_name=u"Coordenada X", max_length=20)
	coordy		 = models.CharField(verbose_name=u"Coordenada Y", max_length=20)
	descripcion  = models.TextField(verbose_name=u"Descripción",blank=True,null=True)
	direccion    = models.TextField(verbose_name=u"Dirección",blank=True,null=True)
	dni    		 = models.CharField(verbose_name=u"Número DNI",max_length=8)
	imgdni       = models.ImageField(verbose_name=u"Imagen DNI",blank=True, null=True,default="no-dni.png")#upload_to='%Y/%m/%d',
	imgpersona   = models.ImageField(verbose_name=u"Imagen de persona",blank=True, null=True,default="no-img.png")#upload_to='%Y/%m/%d',
	imghogar     = models.ImageField(verbose_name=u"Imagen de hogar",blank=True, null=True,default="no-img.png")#upload_to='%Y/%m/%d',
	tipooperacions = models.ManyToManyField(Tipooperacion)
	fecharegistro = models.DateTimeField(auto_now_add=True, blank=True)
	estado       = models.BooleanField(blank=True,default=True)
	
	class Meta:
		ordering = ["apellido"]
	def __str__(self):
		srtApoderado = self.nombre + ' ' + self.apellido
		return srtApoderado

	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150"/>'.format(self.imgdni.url))

	image_tag.short_description = 'Imagen'

	def get_full_name(self,*args,**kwargs):
		nombreCompleto = self.apellido + ', '+ self.nombre
		return nombreCompleto

class Operacion(models.Model):
	personas = models.ManyToManyField(Persona)
	fecha = models.DateTimeField(auto_now_add=True, blank=True)
	imgcomprobante = models.FileField(verbose_name=u"Imagen comprobante",blank=True, null=True,default="no-dni.png")#upload_to='%Y/%m/%d',
	nrooperacion = models.CharField(verbose_name=u"Nro de operación",max_length=20,blank=True,default=0)
	montoayuda = models.IntegerField(verbose_name=u'Monto ayuda',default=0,blank=True)
	montopagado = models.IntegerField(verbose_name=u'Monto ayuda',default=0,blank=True)
	estado = models.IntegerField(blank=True,default=1)
	
	def calcular_porcentaje(self, *args, **kwargs):
		if (self.montopagado):
			porcentaje = (self.montopagado/self.montoayuda)*100
		else:
			porcentaje = 0
		return round(porcentaje)
	def calcular_vencido(self, *args, **Kwargs):
		vencido = False
		if self.fechapagar<date.today() and self.calcular_porcentaje()<100 :
			vencido = True
		return vencido
	def calcular_faltante(self,*args,**kwargs):
		if self.montopagado>0:
				monto_restante = self.montoayuda-self.montopagado
		else:
				monto_restante = self.montoayuda
		return int(monto_restante)

	def save(self, *args, **kwargs):
		print(self)
		super(Operacion, self).save(*args, **kwargs)
		#enviar_datos_operacion(self)

def enviar_datos_operacion(operacion):
	oOpereacion = operacion

	msgData = {}
	msgData["tipoMsg"]= 2
	msgData["message"]= "Nuevo Usuario conectado"
	Enviar_msg(oOpereacion,msgData)
	msgData["tipoMsg"]= 3
	print(str(oOpereacion.personas.all()))
	oPersona = oOpereacion.personas.all()
	msgData["idAyuda"]= oOpereacion.id
	msgData["fecha"]= str(oOpereacion.fecha)
	#msgData["beneficiario"]= oPersona.apellido + ", " + oPersona.nombre
	msgData["beneficiario"]= "Nueva ayuda"
	msgData["imgPersona"]= oPersona.imagen.url
	msgData["beneficiario"]= oPersona.id
	Enviar_msg(self,msgData)
