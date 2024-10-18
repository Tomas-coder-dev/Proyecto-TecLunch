from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Usuario, Comida, Carta, CartaComida, Pedido, Retroalimentacion, Transaccion

# Serializador para el modelo User de Django
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Usando el modelo User de Django
        fields = ['id', 'username', 'email', 'is_staff']  # Incluye solo los campos que necesitas

    def validate_email(self, value):
        """Validar que el correo tenga el dominio @tecsup.edu.pe"""
        if not value.endswith('@tecsup.edu.pe'):
            raise serializers.ValidationError("El correo debe ser del dominio @tecsup.edu.pe")
        return value

    def create(self, validated_data):
        """Crear un nuevo usuario y asegurar que se guarde correctamente"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data.get('password')  # Si pasas la contraseña en validated_data
        )
        return user

# Serializador para el modelo Comida
class ComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comida
        fields = '__all__'

# Serializador para el modelo Carta
class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = '__all__'

# Serializador para el modelo CartaComida
class CartaComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaComida
        fields = '__all__'

# Serializador para el modelo Pedido
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

# Serializador para el modelo Retroalimentacion
class RetroalimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retroalimentacion
        fields = '__all__'

# Serializador para el modelo Transaccion
class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'
