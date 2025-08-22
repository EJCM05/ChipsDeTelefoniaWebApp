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

# Formulario de ventas

class VentaForm(forms.ModelForm):
    # ... (campos del cliente) ...
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.all(),
        label="Seleccionar Lote",
        empty_label="--- Seleccione un lote ---",
        required=True
    )
    
    simcard = forms.ModelChoiceField(
        # El queryset sigue siendo None por defecto
        queryset=SimCard.objects.none(),
        label="Seleccionar SIM Card",
        empty_label="--- Seleccione una SIM Card ---",
        required=True
    )
    
    class Meta:
        model = Cliente
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'cedula_identidad', 'fecha_nacimiento', 'telefono', 'correo'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir las clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # --- Solución al error de validación ---
        # Si el formulario se envía (POST), actualiza el queryset del campo simcard
        if 'lote' in self.data:
            try:
                lote_id = int(self.data.get('lote'))
                # Actualiza el queryset con las SIM Cards disponibles para ese lote
                self.fields['simcard'].queryset = SimCard.objects.filter(id_lote=lote_id).exclude(estado='ocupada')
            except (ValueError, TypeError):
                pass  # Si el valor no es un entero, lo ignoramos por ahora