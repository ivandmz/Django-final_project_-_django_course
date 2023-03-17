from django import forms
from .models import Calzado, Vestimenta, Suplemento, Accesorio, Opciones_calzado, Opciones_vestimenta


class VestimentaForm(forms.ModelForm):

    class Meta:
        model = Vestimenta
        exclude = ('categoria',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'foto': forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'info': forms.Textarea(attrs={'class':'form-control'}),
            'subcategoria': forms.Select(attrs={'class':'form-control','choices': Vestimenta.SUBCATEGORIA}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
        }

class Opcion_vestimentaForm(forms.ModelForm):

    class Meta:
        model = Opciones_vestimenta
        fields = ('talle','stock')
        widgets = {
            'talle': forms.Select(attrs={'class':'form-control','choices': Opciones_vestimenta.TALLES}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
        }

VestimentaOpcionesFormset = forms.inlineformset_factory(
    Vestimenta, 
    Opciones_vestimenta, 
    fields=('talle', 'stock'),
    widgets = {
            'talle': forms.Select(attrs={'class':'form-control','choices': Opciones_vestimenta.TALLES}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
    },
    extra=5,
    max_num=5,
)

#-----------------------------------------------------------------------------------------------------

class CalzadoForm(forms.ModelForm):
    
    class Meta:
        model = Calzado
        second_model = Opciones_calzado
        fields = ('nombre','precio','foto','info','sexo') #,'talle','stock') #exclude = 'calzado'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'foto': forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'info': forms.Textarea(attrs={'class':'form-control'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
        }

class Opcion_calzadoForm(forms.ModelForm):

    class Meta:
        model = Opciones_calzado
        fields = ('talle','stock')
        widgets = {
            'talle': forms.Select(attrs={'class':'form-control','choices': Opciones_calzado.TALLES}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
        }

CalzadoOpcionesFormset = forms.inlineformset_factory(
    Calzado, 
    Opciones_calzado, 
    fields=('talle', 'stock'),
    widgets = {
            'talle': forms.Select(attrs={'class':'form-control','choices': Opciones_calzado.TALLES}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
    },
    extra=12,
    max_num=12,
)

#-----------------------------------------------------------------------------------------------------

class AccesorioForm(forms.ModelForm):

    class Meta:
        model = Accesorio
        exclude = ('categoria',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'foto': forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'info': forms.Textarea(attrs={'class':'form-control'}),
            'subcategoria': forms.Select(attrs={'class':'form-control','choices': Accesorio.SUBCATEGORIA}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
        }
    
#-----------------------------------------------------------------------------------------------------

class SuplementoForm(forms.ModelForm):

    class Meta:
        model = Suplemento
        exclude = ('categoria',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'foto': forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'info': forms.Textarea(attrs={'class':'form-control'}),
            'subcategoria': forms.Select(attrs={'class':'form-control','choices': Suplemento.SUBCATEGORIA}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
        }
    

#---------------------------------------------------------------------------------------------
    
class FormContacto(forms.Form):
    nombre = forms.CharField(
        label='Tu nombre',
        required=False,
        max_length=150,
        widget=forms.TextInput(
            attrs={'class':'form-control white-text'}) #,'placeholder':'Ingresa tu nombre aquí'})
    )
    mail = forms.EmailField(
        label='Tu email',
        max_length=150,
        error_messages={'required':'Por favor completa este campo',},
        widget=forms.TextInput(
            attrs={'class':'form-control','type':'email'})
    )
    mensaje = forms.CharField(
        label='Tu mensaje',
        max_length=600,
        widget=forms.Textarea(
            attrs={'class':'form-control md-textarea white-text','rows':3})
    )