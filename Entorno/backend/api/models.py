from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Personal', 'Personal'),
        ('Administrador', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    preferencias_alimenticias = models.TextField(blank=True)  # Eliminado null=True
    restricciones_dieteticas = models.TextField(blank=True)  # Eliminado null=True
    habitos_consumo = models.TextField(blank=True)  # Eliminado null=True

class Comida(models.Model):
    CATEGORIA_CHOICES = [
        ('Vegetariano', 'Vegetariano'),
        ('No Vegetariano', 'No Vegetariano'),
        ('Vegano', 'Vegano'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    ingredientes = models.TextField()
    calorias = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    disponible = models.BooleanField(default=True)

class Carta(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(unique=True)
    disponible = models.BooleanField(default=True)

class CartaComida(models.Model):
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('Reservado', 'Reservado'),
        ('Pagado', 'Pagado'),
        ('Cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES)
    cantidad = models.IntegerField(default=1)

class Retroalimentacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)  # Eliminado null=True
    calificacion = models.IntegerField()

class Transaccion(models.Model):
    METODO_PAGO_CHOICES = [
        ('Stripe', 'Stripe'),
        ('PayPal', 'PayPal'),
        ('Otro', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completado', 'Completado'),
        ('Fallido', 'Fallido'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
