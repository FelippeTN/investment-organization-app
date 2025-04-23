from django.urls import path
from .views import dashboard, register, asset_list, asset_create, asset_delete, operation_create
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', register, name='register'),
    
    path('ativos/', asset_list, name='asset_list'),
    path('ativos/novo/', asset_create, name='asset_create'),
    path('ativos/excluir/<int:pk>/', asset_delete, name='asset_delete'),
    path('operacoes/novo/', operation_create, name='operation_create'),
]