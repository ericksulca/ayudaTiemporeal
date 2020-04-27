from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from ayuda.models import *
from django.forms.widgets import CheckboxSelectMultiple
from dal import autocomplete

from string import Template
from django.utils.safestring import mark_safe
from dal import autocomplete

class PersonaModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.get_full_name()


class OperacionForm(ModelForm):
	personas = PersonaModelChoiceField(queryset=Persona.objects.all(), label='Manager', required=True)
	class Meta:
		model = Operacion
		fields = ('montoayuda',)
		widgets = {
		'personas': autocomplete.ModelSelect2Multiple(attrs={'class': 'form-control'}, url='persona-autocomplete'),
		'montoayuda': forms.TextInput(attrs={'type': 'number','class': 'form-control'}),
		#'apoderados': autocomplete.ModelSelect2Multiple(url='apoderado-autocomplete')		
		}

class OperacionForm2(ModelForm):
	personas = forms.ModelMultipleChoiceField(queryset=Persona.objects.all())
	class Meta:
		#imagen = models.ImageField(widget=PictureWidget)
		model = Operacion
		fields = ('montoayuda',)
		widgets = {
		#'personas': autocomplete.ModelSelect2Multiple(attrs={'class': 'form-control'}, url='persona-autocomplete'),
		'montoayuda': forms.TextInput(attrs={'type': 'number','class': 'form-control'}),
		
		#'apoderados': autocomplete.ModelSelect2Multiple(url='apoderado-autocomplete')		
		}
	def __init__(self, letter):
		choices = getChoices(letter)
		self.fields['personas'].queryset = choices
