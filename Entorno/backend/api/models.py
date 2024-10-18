from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, rol, contraseña=None):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")

        usuario = self.model(
            correo=self.normalize_email(correo),
            nombre=nombre,
            rol=rol,
        )

        if contraseña:
            usuario.set_password(contraseña)  # Asignar la contraseña de manera segura
        else:
            usuario.set_password(None)  # Permitir cuentas sin contraseña temporalmente
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, rol, contraseña=None):
        usuario = self.create_user(
            correo,
            nombre=nombre,
            rol=rol,
            contraseña=contraseña
        )
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    ROL_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Personal', 'Personal'),
        ('Administrador', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    preferencias_alimenticias = models.TextField(blank=True)
    restricciones_dieteticas = models.TextField(blank=True)
    habitos_consumo = models.TextField(blank=True)
    contraseña = models.CharField(max_length=128, null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return self.nombre

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
    calificacion_promedio = models.FloatField(default=0)  # Calificación promedio
    votos = models.IntegerField(default=0)  # Número de votos
    imagen = models.ImageField(upload_to='comidas/', null=True, blank=True)  # Imagen de la comida

    def __str__(self):
        return self.nombre

class Carta(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(unique=True)
    disponible = models.BooleanField(default=True)
    comidas = models.ManyToManyField(Comida, through='CartaComida')  # Relación con las comidas

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"

class CartaComida(models.Model):
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.carta.nombre} - {self.comida.nombre}"

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

    def __str__(self):
        return f"Pedido de {self.usuario.nombre} - {self.estado}"

class Retroalimentacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)
    calificacion = models.IntegerField()

    def __str__(self):
        return f"Retroalimentación de {self.usuario.nombre} para {self.comida.nombre}"

    def save(self, *args, **kwargs):
        if self.calificacion < 1 or self.calificacion > 5:
            raise ValueError("La calificación debe estar entre 1 y 5")

        # Actualizar la calificación promedio
        comida = self.comida
        total_votos = comida.votos + 1
        nueva_calificacion_promedio = (
            (comida.calificacion_promedio * comida.votos) + self.calificacion
        ) / total_votos

        comida.calificacion_promedio = nueva_calificacion_promedio
        comida.votos = total_votos
        comida.save()

        super().save(*args, **kwargs)

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

    def __str__(self):
        return f"Transacción de {self.pedido.usuario.nombre} - {self.estado}"
