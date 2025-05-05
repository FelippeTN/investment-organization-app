from django.urls import path, include
from .views import *
from .api.api_views import AssetPriceListView, AssetPriceUpdateView
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Asset Price API",
        default_version='v1',
        description="API for fetching and updating asset prices",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('', welcome_page, name='welcome_page'),
    path('home/', home_page, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', register, name='register'),
    path('operacoes/novo/', operation_create, name='operation_create'),
    path('api/assets/prices/', AssetPriceListView.as_view(), name='asset_price_list'),
    path('api/assets/prices/update/', AssetPriceUpdateView.as_view(), name='asset_price_update'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
