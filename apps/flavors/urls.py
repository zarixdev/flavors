from django.urls import path
from . import views, views_admin

app_name = 'flavors'

urlpatterns = [
    # Public views
    path('', views.homepage, name='homepage'),

    # Admin views
    path('admin/login/', views_admin.admin_login, name='admin_login'),
    path('admin/logout/', views_admin.admin_logout, name='admin_logout'),
    path('admin/', views_admin.admin_dashboard, name='admin_dashboard'),

    # Daily selection - MUST be before flavor_detail to avoid path conflict
    path('admin/dzis/', views_admin.daily_selection, name='admin_daily_selection'),
    path('admin/dzis/toggle/<int:flavor_id>/', views_admin.toggle_flavor, name='admin_toggle_flavor'),
    path('admin/dzis/hit/<int:flavor_id>/', views_admin.set_hit, name='admin_set_hit'),
    path('admin/dzis/move/<int:flavor_id>/<str:direction>/', views_admin.move_flavor, name='admin_move_flavor'),
    path('admin/dzis/copy-yesterday/', views_admin.copy_from_yesterday, name='admin_copy_yesterday'),
    path('admin/dzis/clear/', views_admin.clear_selection, name='admin_clear_selection'),
    path('admin/dzis/sort/', views_admin.daily_selection_sort, name='admin_daily_selection_sort'),

    # Flavor CRUD
    path('admin/flavors/', views_admin.flavor_list, name='admin_flavor_list'),
    path('admin/flavors/create/', views_admin.flavor_create, name='admin_flavor_create'),
    path('admin/flavors/archived/', views_admin.archived_flavors, name='admin_archived_flavors'),
    path('admin/flavors/<int:pk>/', views_admin.flavor_detail, name='admin_flavor_detail'),
    path('admin/flavors/<int:pk>/edit/', views_admin.flavor_edit, name='admin_flavor_edit'),
    path('admin/flavors/<int:pk>/archive/', views_admin.archive_flavor, name='admin_flavor_archive'),
    path('admin/flavors/<int:pk>/restore/', views_admin.restore_flavor, name='admin_flavor_restore'),
]
