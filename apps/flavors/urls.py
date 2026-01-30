from django.urls import path
from . import views, views_admin

urlpatterns = [
    # Public views
    path('', views.index, name='index'),

    # Admin views
    path('admin/login/', views_admin.admin_login, name='admin_login'),
    path('admin/logout/', views_admin.admin_logout, name='admin_logout'),
    path('admin/', views_admin.admin_dashboard, name='admin_dashboard'),
]
