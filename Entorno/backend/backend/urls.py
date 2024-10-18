from django.contrib import admin  # Importar el módulo admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views  # Importa todas las vistas desde api

# Definir el router para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'comidas', views.ComidaViewSet)
router.register(r'cartas', views.CartaViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'retroalimentaciones', views.RetroalimentacionViewSet)
router.register(r'transacciones', views.TransaccionViewSet)

urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

    # Rutas API gestionadas por el router de DRF
    path('api/', include(router.urls)),

    # Ruta para el login personalizado
    path('api/login/', views.CustomLoginView.as_view(), name='custom_login'),

    # Ruta para la creación de usuarios (solo administradores)
    path('api/crear_usuario/', views.CrearUsuarioView.as_view(), name='crear_usuario'),
]
