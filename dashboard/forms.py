from django import forms
from core.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
# ==========================================
# Formulario Para crear lotes
# ==========================================

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['nombre_lote', 'max_simcard', 'fecha_creacion']
        
        # Agregamos widgets para personalizar la presentación
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={
                    'type': 'date',  # Esto convierte el campo en un selector de fecha HTML5
                    'class': 'form-control' # Clase de Bootstrap para estilos
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('nombre_lote', css_class='form-control'),
            Field('max_simcard', css_class='form-control'),
            Field('fecha_creacion', css_class='form-control'), # Crispy Forms aplicará esta clase
            Submit('submit', 'Guardar', css_class='btn-primary mt-3')
        )

# ==========================================
# Formulario para crear SIMCards
# ==========================================

class SimCardForm(forms.ModelForm):
    class Meta:
        model = SimCard
        fields = ['codigo', 'estado', 'numero_telefono', 'id_operadora']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'id_operadora': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        # Captura 'lote_pk' de los argumentos antes de llamar a super()
        self.lote_pk = kwargs.pop('lote_pk', None)
        # Ahora la clase base ya no verá 'lote_pk' y no dará error
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('codigo'),
            Field('estado'),
            Field('numero_telefono'),
            Field('id_operadora'),
        )
        
# ==========================================
# formulario para crear operadoras        
# ==========================================

class OperadoraForm(forms.ModelForm):
    class Meta:
        model = Operadora
        fields = ["nombre_operadora", "codigo", "pais"]
        widgets = {
            "nombre_operadora": forms.TextInput(attrs={'class': 'form-control'}),
            "codigo": forms.TextInput(attrs={'class': 'form-control'}),
            "pais": forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("nombre_operadora"),
            Field("codigo"),
            Field("pais"),
        )