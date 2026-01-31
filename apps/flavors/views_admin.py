from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone

from .models import Flavor, DailySelection
from .forms import FlavorForm


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


@login_required
@require_http_methods(["GET"])
def flavor_list(request):
    """List all flavors with filter by status."""
    status_filter = request.GET.get('status', 'active')
    search = request.GET.get('search', '')

    flavors = Flavor.objects.all()
    if status_filter != 'all':
        flavors = flavors.filter(status=status_filter)
    if search:
        flavors = flavors.filter(name__icontains=search)

    flavors = flavors.order_by('-created_at')

    if request.htmx:
        return render(request, 'admin/partials/flavor_list.html', {'flavors': flavors})

    return render(request, 'admin/flavor_list.html', {
        'flavors': flavors,
        'status_filter': status_filter,
    })


@login_required
@require_http_methods(["GET", "POST"])
def flavor_create(request):
    """Create new flavor with HTMX support."""
    if request.method == 'POST':
        form = FlavorForm(request.POST, request.FILES)
        if form.is_valid():
            flavor = form.save()
            messages.success(request, f'Smak "{flavor.name}" dodany.')
            if request.htmx:
                flavors = Flavor.objects.filter(status='active')
                return render(request, 'admin/partials/flavor_list.html', {'flavors': flavors})
            return redirect('admin_flavor_list')

        if request.htmx:
            return render(request, 'admin/partials/flavor_form.html', {
                'form': form, 'submit_url': request.path, 'title': 'Dodaj smak'
            }, status=422)
    else:
        form = FlavorForm()

    return render(request, 'admin/flavor_form.html', {
        'form': form, 'title': 'Dodaj nowy smak', 'submit_url': request.path
    })


@login_required
@require_http_methods(["GET", "POST"])
def flavor_edit(request, pk):
    """Edit existing flavor."""
    flavor = get_object_or_404(Flavor, pk=pk)

    if request.method == 'POST':
        form = FlavorForm(request.POST, request.FILES, instance=flavor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Smak "{flavor.name}" zaktualizowany.')
            return redirect('admin_flavor_list')
    else:
        form = FlavorForm(instance=flavor)

    return render(request, 'admin/flavor_form.html', {
        'form': form, 'flavor': flavor, 'title': f'Edytuj: {flavor.name}', 'submit_url': request.path
    })


@login_required
@require_http_methods(["GET"])
def flavor_detail(request, pk):
    """View flavor details (read-only)."""
    flavor = get_object_or_404(Flavor, pk=pk)
    return render(request, 'admin/flavor_detail.html', {'flavor': flavor})


@login_required
@require_http_methods(["POST"])
def archive_flavor(request, pk):
    """Archive a flavor (soft delete)."""
    flavor = get_object_or_404(Flavor, pk=pk)

    flavor.status = 'archived'
    flavor.save()
    messages.success(request, f'Smak "{flavor.name}" zarchiwizowany.')
    return redirect('admin_flavor_list')


@login_required
@require_http_methods(["POST"])
def restore_flavor(request, pk):
    """Restore an archived flavor to active status."""
    flavor = get_object_or_404(Flavor, pk=pk, status='archived')
    flavor.status = 'active'
    flavor.save()
    messages.success(request, f'Smak "{flavor.name}" przywrócony.')
    return redirect('admin_archived_flavors')


@login_required
@require_http_methods(["GET"])
def archived_flavors(request):
    """List all archived flavors with restore option."""
    flavors = Flavor.objects.filter(status='archived').order_by('name')
    return render(request, 'admin/archived_flavors.html', {'flavors': flavors})
