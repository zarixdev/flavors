from django.urls import path
from . import views, views_admin

urlpatterns = [
    # Public views
    path('', views.index, name='index'),

    # Admin views
    path('admin/login/', views_admin.admin_login, name='admin_login'),
    path('admin/logout/', views_admin.admin_logout, name='admin_logout'),
    path('admin/', views_admin.admin_dashboard, name='admin_dashboard'),

    # Flavor CRUD
    path('admin/flavors/', views_admin.flavor_list, name='admin_flavor_list'),
    path('admin/flavors/create/', views_admin.flavor_create, name='admin_flavor_create'),
    path('admin/flavors/<int:pk>/edit/', views_admin.flavor_edit, name='admin_flavor_edit'),
]
