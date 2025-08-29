from django import forms
from core.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.db.models import Q # Importamos Q para poder usar el OR en el queryset

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
        
# =====================================================
#           formulario para crear operadoras        
# ==================================================

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

# ==============================================
#               Formulario de ventas
# =================================================


class VentaForm(forms.ModelForm):
    # 1. CAMPOS DEL CLIENTE (Añadidos manualmente)
    primer_nombre = forms.CharField(max_length=100, label="Primer Nombre")
    segundo_nombre = forms.CharField(max_length=100, label="Segundo Nombre", required=False)
    primer_apellido = forms.CharField(max_length=100, label="Primer Apellido")
    segundo_apellido = forms.CharField(max_length=100, label="Segundo Apellido", required=False)
    cedula_identidad = forms.CharField(max_length=20, label="Cédula de Identidad")
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Nacimiento")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    correo = forms.EmailField(label="Correo Electrónico")
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Dirección")

    # 2. CAMPO PARA LA SELECCIÓN DE LOTE
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.all(),
        label="Seleccionar Lote",
        required=False
    )

    class Meta:
        model = Venta
        fields = ['id_simcard', 'monto_total']
        labels = {
            'id_simcard': 'Seleccionar SIM Card',
            'monto_total': 'Ingresa El monto de la venta'
        }
        widgets = {
            'id_simcard': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        venta = self.instance

        if venta and venta.pk and venta.id_cliente:
            # Lógica de inicialización para el formulario de EDICIÓN
            cliente = venta.id_cliente
            simcard_actual = venta.id_simcard

            # Cargar los datos del cliente en los campos del formulario
            self.initial['primer_nombre'] = cliente.primer_nombre
            self.initial['segundo_nombre'] = cliente.segundo_nombre
            self.initial['primer_apellido'] = cliente.primer_apellido
            self.initial['segundo_apellido'] = cliente.segundo_apellido
            self.initial['cedula_identidad'] = cliente.cedula_identidad
            self.initial['fecha_nacimiento'] = cliente.fecha_nacimiento
            self.initial['telefono'] = cliente.telefono
            self.initial['correo'] = cliente.correo
            self.initial['direccion'] = cliente.direccion

            if simcard_actual:
                # Establecer el lote inicial basado en la SIM Card actual
                self.initial['lote'] = simcard_actual.id_lote

                # CORRECCIÓN: Configurar un queryset más flexible para incluir cualquier SIM que no esté vendida
                simcards_disponibles = SimCard.objects.filter(id_lote=simcard_actual.id_lote).exclude(estado='vendida')
                simcard_asignada = SimCard.objects.filter(pk=simcard_actual.pk)
                self.fields['id_simcard'].queryset = simcards_disponibles | simcard_asignada

            # CAMBIO: Deshabilitar los campos de producto en modo de edición
            self.fields['lote'].disabled = True
            self.fields['id_simcard'].disabled = True
        else:
            # CORRECCIÓN: Para la creación, el queryset debe incluir todas las SIMs disponibles
            # para que la validación del formulario funcione correctamente.
            self.fields['id_simcard'].queryset = SimCard.objects.exclude(estado='vendida')
            
        # Configuración final de los campos
        self.fields['id_simcard'].label = "Seleccionar SIM Card"
        if 'lote' in self.fields:
             self.fields['lote'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True, user=None):
        # Lógica de guardado personalizada que maneja todos los modelos
        
        # 1. Obtener el cliente actual o crear uno nuevo
        cliente = self.instance.id_cliente if self.instance.pk else Cliente()
        
        # 2. Actualizar los datos del cliente desde el formulario
        for field in ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 
                      'cedula_identidad', 'fecha_nacimiento', 'telefono', 'correo', 'direccion']:
            setattr(cliente, field, self.cleaned_data[field])

        # AÑADIR: Asignar el usuario propietario si es una venta nueva
        if not self.instance.pk and user:
            cliente.id_usuario_propietario = user
            
        cliente.save()

        # 3. Manejar la lógica de las SIM Cards
        simcard_nueva = self.cleaned_data['id_simcard']
        simcard_anterior = self.instance.id_simcard if self.instance.pk else None

        # Verificar si la SIM Card ha cambiado
        if simcard_nueva and simcard_nueva.pk != (simcard_anterior.pk if simcard_anterior else None):
            # Si se cambió la SIM, liberar la anterior (si existía)
            if simcard_anterior:
                simcard_anterior.estado = 'inactiva'
                simcard_anterior.id_cliente = None
                simcard_anterior.numero_telefono = None
                simcard_anterior.save()
            
            # Asignar y vender la nueva SIM Card
            simcard_nueva.estado = 'vendida'
            simcard_nueva.id_cliente = cliente
            simcard_nueva.numero_telefono = cliente.telefono
            simcard_nueva.save()
        elif simcard_nueva and simcard_nueva.pk == (simcard_anterior.pk if simcard_anterior else None):
            # Si la SIM no cambió, solo actualizamos el número de teléfono por si cambió en el formulario
            simcard_nueva.numero_telefono = cliente.telefono
            simcard_nueva.save()

        # 4. Preparar la instancia de Venta para guardarla
        venta = super().save(commit=False)
        venta.id_cliente = cliente
        venta.id_simcard = simcard_nueva
        if user:
            venta.id_usuario_propietario = user
        
        if commit:
            venta.save()
            
        return venta
