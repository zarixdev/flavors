import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse

from .models import Flavor, DailySelection
from .forms import FlavorForm

logger = logging.getLogger(__name__)


def admin_login(request):
    """Custom login view for ice cream shop owner."""
    if request.user.is_authenticated:
        return redirect('flavors:admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flavors:admin_dashboard')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło.')
    return render(request, 'admin/login.html')


@staff_member_required
@require_http_methods(["POST"])
def admin_logout(request):
    """Logout view."""
    logout(request)
    return redirect('flavors:admin_login')


@staff_member_required
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


@staff_member_required
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


@staff_member_required
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
            return redirect('flavors:admin_flavor_list')

        if request.htmx:
            return render(request, 'admin/partials/flavor_form.html', {
                'form': form, 'submit_url': request.path, 'title': 'Dodaj smak'
            }, status=422)
    else:
        form = FlavorForm()

    return render(request, 'admin/flavor_form.html', {
        'form': form, 'title': 'Dodaj nowy smak', 'submit_url': request.path
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def flavor_edit(request, pk):
    """Edit existing flavor."""
    flavor = get_object_or_404(Flavor, pk=pk)

    if request.method == 'POST':
        form = FlavorForm(request.POST, request.FILES, instance=flavor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Smak "{flavor.name}" zaktualizowany.')
            return redirect('flavors:admin_flavor_list')
    else:
        form = FlavorForm(instance=flavor)

    return render(request, 'admin/flavor_form.html', {
        'form': form, 'flavor': flavor, 'title': f'Edytuj: {flavor.name}', 'submit_url': request.path
    })


@staff_member_required
@require_http_methods(["GET"])
def flavor_detail(request, pk):
    """View flavor details (read-only)."""
    flavor = get_object_or_404(Flavor, pk=pk)
    return render(request, 'admin/flavor_detail.html', {'flavor': flavor})


@staff_member_required
@require_http_methods(["POST"])
def archive_flavor(request, pk):
    """Archive a flavor (soft delete)."""
    flavor = get_object_or_404(Flavor, pk=pk)

    flavor.status = 'archived'
    flavor.save()
    messages.success(request, f'Smak "{flavor.name}" zarchiwizowany.')
    return redirect('flavors:admin_flavor_list')


@staff_member_required
@require_http_methods(["POST"])
def restore_flavor(request, pk):
    """Restore an archived flavor to active status."""
    flavor = get_object_or_404(Flavor, pk=pk, status='archived')
    flavor.status = 'active'
    flavor.save()
    messages.success(request, f'Smak "{flavor.name}" przywrócony.')
    return redirect('flavors:admin_archived_flavors')


@staff_member_required
@require_http_methods(["GET"])
def archived_flavors(request):
    """List all archived flavors with restore option."""
    flavors = Flavor.objects.filter(status='archived').order_by('name')
    return render(request, 'admin/archived_flavors.html', {'flavors': flavors})


# ============================================================================
# DAILY SELECTION VIEWS
# ============================================================================

@staff_member_required
@require_http_methods(["GET"])
def daily_selection(request):
    """
    Main daily selection interface.
    Shows all active flavors with their selection state for today.
    """
    today = timezone.now().date()
    selection, created = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    # Get all active flavors
    all_flavors = Flavor.objects.filter(status='active').order_by('name')

    # Get selected flavor IDs for efficient lookup
    selected_ids = set(selection.flavors.values_list('id', flat=True))

    # Build list with selection state
    flavors_with_state = []
    for flavor in all_flavors:
        flavors_with_state.append({
            'flavor': flavor,
            'is_selected': flavor.id in selected_ids,
            'is_hit': selection.hit_of_the_day_id == flavor.id,
        })

    # Get ordered flavors for display
    selected_flavors = selection.get_ordered_flavors()

    context = {
        'selection': selection,
        'flavors': flavors_with_state,
        'selected_flavors': selected_flavors,
        'all_flavors': all_flavors,
        'today': today,
        'selected_count': len(selected_ids),
    }

    if request.htmx:
        return render(request, 'admin/partials/daily_selection.html', context)

    return render(request, 'admin/daily_selection.html', context)


@staff_member_required
@require_http_methods(["POST"])
def toggle_flavor(request, flavor_id):
    """
    Toggle a flavor in/out of today's selection.
    Returns partial row template with updated state.
    """
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    flavor = get_object_or_404(Flavor, pk=flavor_id, status='active')

    # Check if flavor is currently selected
    is_selected = selection.flavors.filter(pk=flavor_id).exists()

    try:
        if is_selected:
            # Remove from selection
            selection.flavors.remove(flavor)
            selection.remove_flavor_from_order(flavor_id)

            # If this was the hit, clear it
            if selection.hit_of_the_day_id == flavor_id:
                selection.hit_of_the_day = None
                selection.save(update_fields=['hit_of_the_day'])

            # Silent for HTMX requests - visual state change is feedback enough
            if not request.htmx:
                messages.info(request, f'Usunięto: {flavor.name}')
        else:
            # Add to selection
            selection.flavors.add(flavor)
            selection.add_flavor_to_order(flavor_id)
            # Silent for HTMX requests - visual state change is feedback enough
            if not request.htmx:
                messages.success(request, f'Dodano: {flavor.name}')

        # Update last_updated timestamp
        selection.last_updated = timezone.now()
        selection.save(update_fields=['last_updated'])

        # Refresh selection state
        is_selected = not is_selected

    except Exception as e:
        logger.error(f"Error in toggle_flavor for flavor_id={flavor_id}: {e}")
        # Errors always show, regardless of HTMX
        messages.error(request, 'Nie udało się zaktualizować wyboru. Spróbuj ponownie.')

    # Refresh selected_ids after toggle for counter context
    selected_ids = set(selection.flavors.values_list('id', flat=True))

    context = {
        'flavor': flavor,
        'is_selected': is_selected if 'is_selected' in locals() else False,
        'selection': selection,
        'selected_count': len(selected_ids),
        'total_count': Flavor.objects.filter(status='active').count(),
        'hit_name': selection.hit_of_the_day.name if selection.hit_of_the_day else None,
    }

    return render(request, 'admin/partials/toggle_response.html', context)


@staff_member_required
@require_http_methods(["POST"])
def set_hit(request, flavor_id):
    """
    Set or toggle hit of the day.
    If flavor is already hit: clear it.
    If different flavor: set as new hit.
    """
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    flavor = get_object_or_404(Flavor, pk=flavor_id, status='active')

    # Verify flavor is in today's selection
    if not selection.flavors.filter(pk=flavor_id).exists():
        messages.error(request, 'Wybierz najpierw ten smak, aby ustawić hit dnia.')
        return _get_selection_partial(request, selection)

    try:
        # Toggle hit state
        if selection.hit_of_the_day_id == flavor_id:
            selection.hit_of_the_day = None
            selection.save(update_fields=['hit_of_the_day'])
            # Silent for HTMX requests - visual state change is feedback enough
            if not request.htmx:
                messages.info(request, f'Usunięto hit dnia: {flavor.name}')
        else:
            selection.hit_of_the_day = flavor
            selection.save(update_fields=['hit_of_the_day'])
            # Silent for HTMX requests - visual state change is feedback enough
            if not request.htmx:
                messages.success(request, f'Hit dnia: {flavor.name}')

        # Update last_updated timestamp
        selection.last_updated = timezone.now()
        selection.save(update_fields=['last_updated'])
    except Exception as e:
        logger.error(f"Error in set_hit for flavor_id={flavor_id}: {e}")
        # Errors always show, regardless of HTMX
        messages.error(request, 'Nie udało się ustawić hitu dnia. Spróbuj ponownie.')

    return _get_selection_partial(request, selection)


@staff_member_required
@require_http_methods(["POST"])
def move_flavor(request, flavor_id, direction):
    """
    Move flavor up or down in the display order.
    direction: 'up' (-1) or 'down' (+1)
    """
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    # Convert direction string to numeric offset
    direction_map = {'up': -1, 'down': 1}
    direction_value = direction_map.get(direction, 0)

    if direction_value == 0:
        messages.error(request, 'Nieprawidłowy kierunek.')
        return _get_selection_partial(request, selection)

    try:
        # Perform the move
        success = selection.move_flavor(flavor_id, direction_value)

        if success:
            flavor = get_object_or_404(Flavor, pk=flavor_id)
            direction_label = 'wyżej' if direction_value == -1 else 'niżej'
            messages.success(request, f'Przesunięto {flavor.name} {direction_label}')
        else:
            messages.info(request, 'Nie można przesunąć dalej.')
    except Exception as e:
        logger.error(f"Error in move_flavor for flavor_id={flavor_id}, direction={direction}: {e}")
        messages.error(request, 'Nie udało się zmienić kolejności. Spróbuj ponownie.')

    return _get_selection_partial(request, selection, sort_mode=True)


@staff_member_required
@require_http_methods(["POST"])
def copy_from_yesterday(request):
    """
    Copy yesterday's selection to today.
    Copies flavors and display_order.
    """
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    try:
        yesterday_selection = DailySelection.objects.get(date=yesterday)
    except DailySelection.DoesNotExist:
        messages.warning(request, 'Brak wyboru z wczoraj do skopiowania.')
        return _get_selection_partial(request, selection)

    # Get yesterday's flavors (only active ones)
    yesterday_flavors = yesterday_selection.flavors.filter(status='active')
    flavor_count = yesterday_flavors.count()

    if flavor_count == 0:
        messages.info(request, 'Wczorajszy wybór był pusty lub wszystkie smaki zostały zarchiwizowane.')
        return _get_selection_partial(request, selection)

    try:
        # Clear current selection
        selection.flavors.clear()
        selection.hit_of_the_day = None

        # Copy flavors
        selection.flavors.set(yesterday_flavors)

        # Copy display_order (filter to only include active flavors that exist)
        active_ids = set(yesterday_flavors.values_list('id', flat=True))
        new_order = [fid for fid in (yesterday_selection.display_order or []) if fid in active_ids]

        # Add any flavors not in the order (append at end)
        for flavor in yesterday_flavors:
            if flavor.id not in new_order:
                new_order.append(flavor.id)

        selection.display_order = new_order
        selection.last_updated = timezone.now()
        selection.save(update_fields=['display_order', 'hit_of_the_day', 'last_updated'])

        messages.success(request, f'Skopiowano {flavor_count} smaków z wczoraj.')
    except Exception as e:
        logger.error(f"Error in copy_from_yesterday: {e}")
        messages.error(request, 'Nie udało się skopiować wczorajszego wyboru. Spróbuj ponownie.')

    return _get_selection_partial(request, selection)


@staff_member_required
@require_http_methods(["POST"])
def clear_selection(request):
    """
    Clear today's selection - remove all flavors and reset hit.
    """
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    count = selection.flavors.count()

    try:
        selection.flavors.clear()
        selection.hit_of_the_day = None
        selection.display_order = []
        selection.last_updated = timezone.now()
        selection.save(update_fields=['hit_of_the_day', 'display_order', 'last_updated'])
        # Silent for HTMX requests - visual state change is feedback enough
        if not request.htmx:
            messages.info(request, f'Wyczyszczono wybór ({count} smaków).')
    except Exception as e:
        logger.error(f"Error in clear_selection: {e}")
        # Errors always show, regardless of HTMX
        messages.error(request, 'Nie udało się wyczyścić wyboru. Spróbuj ponownie.')

    return _get_selection_partial(request, selection)


@staff_member_required
@require_http_methods(["GET"])
def daily_selection_sort(request):
    """Sort mode for reordering selected flavors."""
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    selected_flavors = selection.get_ordered_flavors()

    return render(request, 'admin/partials/selection_sort.html', {
        'selection': selection,
        'selected_flavors': selected_flavors,
    })


@staff_member_required
@require_http_methods(["POST"])
def reorder_flavors(request):
    """
    Reorder selected flavors based on sortable POST data.
    Expects form data with 'flavor_order' containing ordered flavor IDs.
    """
    today = timezone.now().date()
    selection, _ = DailySelection.objects.get_or_create(
        date=today,
        defaults={'display_order': []}
    )

    # Get ordered IDs from form data (htmx-sort sends: flavor_order=1&flavor_order=3...)
    ordered_ids = request.POST.getlist('flavor_order')

    if not ordered_ids:
        messages.error(request, 'Nie przesłano nowej kolejności.')
        return _get_selection_partial(request, selection, sort_mode=True)

    try:
        # Convert to integers
        ordered_ids = [int(fid) for fid in ordered_ids]

        # Validate all selected flavors are present
        selected_ids = set(selection.flavors.values_list('id', flat=True))
        received_ids = set(ordered_ids)

        if received_ids != selected_ids:
            messages.error(request, 'Nieprawidłowa kolejność - brakujące lub dodatkowe smaki.')
            return _get_selection_partial(request, selection, sort_mode=True)

        # Save new order
        selection.display_order = ordered_ids
        selection.save(update_fields=['display_order'])
        messages.success(request, 'Kolejność została zaktualizowana.')

    except (ValueError, TypeError) as e:
        logger.error(f"Error parsing flavor order: {e}")
        messages.error(request, 'Nieprawidłowy format danych.')
    except Exception as e:
        logger.error(f"Error in reorder_flavors: {e}")
        messages.error(request, 'Nie udało się zmienić kolejności. Spróbuj ponownie.')

    return _get_selection_partial(request, selection, sort_mode=True)


def _get_selection_partial(request, selection, sort_mode=False):
    """
    Helper to return the selection list partial with context.
    Used by multiple endpoints after making changes.
    """
    # Get all active flavors
    all_flavors = Flavor.objects.filter(status='active').order_by('name')

    # Get selected flavor IDs
    selected_ids = set(selection.flavors.values_list('id', flat=True))

    # Build list with selection state
    flavors_with_state = []
    for flavor in all_flavors:
        flavors_with_state.append({
            'flavor': flavor,
            'is_selected': flavor.id in selected_ids,
            'is_hit': selection.hit_of_the_day_id == flavor.id,
        })

    # Get ordered flavors for display
    selected_flavors = selection.get_ordered_flavors()

    context = {
        'selection': selection,
        'flavors': flavors_with_state,
        'selected_flavors': selected_flavors,
        'all_flavors': all_flavors,
        'today': selection.date,
        'selected_count': len(selected_ids),
        'sort_mode': sort_mode,
    }

    if sort_mode:
        return render(request, 'admin/partials/selection_sort.html', context)

    return render(request, 'admin/partials/selection_list.html', context)
