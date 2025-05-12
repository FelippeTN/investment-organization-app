from django.urls import path
from .views import *
from .api.api_views import *
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Asset Price API",
        default_version='v1',
        contact=openapi.Contact(email="felippenalim2004@gmail.com"),
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
    path('ai_chat/', ai_consult, name='ai_consult'),
    
    #path('api/ai_response', AIAgentRequest.as_view(), name='ai_agent'),
    path('api/assets/prices/', AssetPriceListView.as_view(), name='asset_price_list'),
    path('api/assets/prices/update/', AssetPriceUpdateView.as_view(), name='asset_price_update'),
    path('api/assets/tickers/update/', AssetTickerCreateView.as_view(), name='asset_ticker_update'),
    path('api/assets/sectors/update/', AssetSectorUpdateView.as_view(), name='asset_sector_update'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]