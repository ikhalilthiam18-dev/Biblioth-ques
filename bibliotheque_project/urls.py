from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from api.views import HomeView

# Personalisation de l'admin
admin.site.site_header = "Bibliothèque — Administration"
admin.site.site_title = "Bibliothèque Admin"
admin.site.index_title = "Tableau de bord"

urlpatterns = [
    # Page d'accueil moderne
    path('', HomeView.as_view(), name='home'),

    path('admin/', admin.site.urls),

    # API principale
    path('api/', include('api.urls')),

    # Browsable API DRF
    path('api-auth/', include('rest_framework.urls')),

    # JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OpenAPI Schema + Swagger + Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
