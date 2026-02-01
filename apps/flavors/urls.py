from django.urls import path
from . import views, views_admin

app_name = 'flavors'

urlpatterns = [
    # Public views
    path('', views.homepage, name='homepage'),

    # Admin views (using /panel/ prefix to avoid Django Admin URL conflict)
    path('panel/login/', views_admin.admin_login, name='admin_login'),
    path('panel/logout/', views_admin.admin_logout, name='admin_logout'),
    path('panel/', views_admin.admin_dashboard, name='admin_dashboard'),

    # Daily selection - MUST be before flavor_detail to avoid path conflict
    path('panel/dzis/', views_admin.daily_selection, name='admin_daily_selection'),
    path('panel/dzis/toggle/<int:flavor_id>/', views_admin.toggle_flavor, name='admin_toggle_flavor'),
    path('panel/dzis/hit/<int:flavor_id>/', views_admin.set_hit, name='admin_set_hit'),
    path('panel/dzis/move/<int:flavor_id>/<str:direction>/', views_admin.move_flavor, name='admin_move_flavor'),
    path('panel/dzis/copy-yesterday/', views_admin.copy_from_yesterday, name='admin_copy_yesterday'),
    path('panel/dzis/clear/', views_admin.clear_selection, name='admin_clear_selection'),
    path('panel/dzis/sort/', views_admin.daily_selection_sort, name='admin_daily_selection_sort'),

    # Flavor CRUD
    path('panel/flavors/', views_admin.flavor_list, name='admin_flavor_list'),
    path('panel/flavors/create/', views_admin.flavor_create, name='admin_flavor_create'),
    path('panel/flavors/archived/', views_admin.archived_flavors, name='admin_archived_flavors'),
    path('panel/flavors/<int:pk>/', views_admin.flavor_detail, name='admin_flavor_detail'),
    path('panel/flavors/<int:pk>/edit/', views_admin.flavor_edit, name='admin_flavor_edit'),
    path('panel/flavors/<int:pk>/archive/', views_admin.archive_flavor, name='admin_flavor_archive'),
    path('panel/flavors/<int:pk>/restore/', views_admin.restore_flavor, name='admin_flavor_restore'),
]
