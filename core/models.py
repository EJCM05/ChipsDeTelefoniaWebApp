from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. Usuarios / DjangoAuth
# Se extiende AbstractUser para usar las funcionalidades de autenticación de Django


class Usuario(AbstractUser):
    # Solución al error: Usar related_name='+' para deshabilitar los accesorios inversos
    # y evitar el conflicto.
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="+",  # Deshabilita la relación inversa en 'Group'
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="+",  # Deshabilita la relación inversa en 'Permission'
        blank=True,
        help_text="Specific permissions for this user.",
    )

    ROL_CHOICES = (
        ("administrador", "Administrador"),
        ("supervisor", "Supervisor"),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="supervisor")

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


# 2. Operadora
class Operadora(models.Model):
    nombre_operadora = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_operadora


# 3. Lotes
class Lote(models.Model):
    max_simcard = models.IntegerField(default=50)
    nombre_lote = models.CharField(max_length=20)
    fecha_creacion = models.DateField()
    id_usuario_propietario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="lotes"
    )

    def __str__(self):
        return f'{self.nombre_lote}'


# 4. Clientes
class Cliente(models.Model):
    primer_nombre = models.CharField(max_length=15)
    segundo_nombre = models.CharField(max_length=15, blank=True, null=True)
    primer_apellido = models.CharField(max_length=15)
    segundo_apellido = models.CharField(max_length=15, blank=True, null=True)
    cedula_identidad = models.CharField(max_length=25)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=35)
    correo = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_usuario_propietario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="clientes"
    )
    direccion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"


# 5. SimCards
class SimCard(models.Model):
    # Definimos las opciones de estado de la SIM
    ESTADO_CHOICES = (
        ("activa", "Activa"),
        ("inactiva", "Inactiva"),
        ("pendiente", "Pendiente de activación"),
        ("perdida", "Perdida"),
        ("robada", "Robada"),
        ("desactivada", "Desactivada"),
        ("vendida", "Vendida")
    )
    codigo = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="inactiva")
    numero_telefono = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Claves foráneas (FK)
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="simcards",
    )
    id_lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name="simcards")
    id_operadora = models.ForeignKey(
        Operadora, on_delete=models.CASCADE, related_name="simcards"
    )

    def __str__(self):
        return self.codigo

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    
    # Claves foráneas (FK)
    id_cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="ventas"
    )
    id_simcard = models.ForeignKey(
        SimCard, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="ventas"
    )
    id_usuario_propietario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name="ventas"
    )

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.id_cliente.primer_nombre} {self.id_cliente.primer_apellido}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"