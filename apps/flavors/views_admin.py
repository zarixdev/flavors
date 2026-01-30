from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone

from .models import Flavor, DailySelection


def admin_login(request):
    """Custom login view for ice cream shop owner."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło.')
    return render(request, 'admin/login.html')


def admin_logout(request):
    """Logout view."""
    logout(request)
    return redirect('admin_login')


@login_required
@require_http_methods(["GET"])
def admin_dashboard(request):
    """Main admin dashboard - list flavors and daily selection status."""
    flavors = Flavor.objects.filter(status='active').order_by('-created_at')
    today = timezone.now().date()
    today_selection = DailySelection.objects.filter(date=today).first()

    context = {
        'flavors': flavors,
        'today_selection': today_selection,
        'flavor_count': flavors.count(),
    }

    if request.htmx:
        return render(request, 'admin/partials/dashboard_content.html', context)

    return render(request, 'admin/dashboard.html', context)
