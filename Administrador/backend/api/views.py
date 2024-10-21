from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario, Comida, Carta, CartaComida, Pedido, Retroalimentacion, Transaccion
from .serializers import UsuarioSerializer, ComidaSerializer, CartaSerializer, CartaComidaSerializer, PedidoSerializer, RetroalimentacionSerializer, TransaccionSerializer

# ViewSets para los modelos
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ComidaViewSet(viewsets.ModelViewSet):
    queryset = Comida.objects.all()
    serializer_class = ComidaSerializer

class CartaViewSet(viewsets.ModelViewSet):
    queryset = Carta.objects.all()
    serializer_class = CartaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

# Otras vistas similares para Retroalimentacion y Transaccion...
class RetroalimentacionViewSet(viewsets.ModelViewSet):
    queryset = Retroalimentacion.objects.all()
    serializer_class = RetroalimentacionSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer

# Vista personalizada de login
class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificar si el email tiene el dominio @tecsup.edu.pe
        if not email.endswith('@tecsup.edu.pe'):
            return Response({"error": "Solo se permiten correos @tecsup.edu.pe"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario está en la base de datos (lista blanca)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuario no autorizado"}, status=status.HTTP_400_BAD_REQUEST)

        # Autenticar usuario
        user = authenticate(username=user.username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'role': 'admin' if user.is_staff else 'user'
                }
            })
        else:
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)

# Vista protegida para que solo los administradores puedan crear usuarios
class CrearUsuarioView(APIView):
    permission_classes = [IsAdminUser]  # Solo permite a administradores

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificar si el correo tiene el dominio @tecsup.edu.pe
        if not email.endswith('@tecsup.edu.pe'):
            return Response({"error": "El correo debe ser del dominio @tecsup.edu.pe"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({"success": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
