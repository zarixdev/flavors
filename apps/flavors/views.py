from django.shortcuts import render
from django.utils import timezone

from .models import DailySelection, Flavor


def homepage(request):
    """
    Widok głównej strony wyświetlający dzisiejsze smaki.
    Z logiką fallback: dzisiaj -> wczoraj -> wszystkie aktywne.
    """
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    flavors = []
    hit_of_the_day = None
    last_updated = None
    fallback_note = None

    # Próba pobrania dzisiejszego zestawu
    try:
        selection = DailySelection.objects.select_related(
            'hit_of_the_day'
        ).prefetch_related('flavors').get(date=today)

        flavors = list(selection.flavors.all())
        hit_of_the_day = selection.hit_of_the_day
        last_updated = selection.updated_at

    except DailySelection.DoesNotExist:
        # Fallback: wczorajszy zestaw
        try:
            selection = DailySelection.objects.select_related(
                'hit_of_the_day'
            ).prefetch_related('flavors').get(date=yesterday)

            flavors = list(selection.flavors.all())
            hit_of_the_day = selection.hit_of_the_day
            last_updated = selection.updated_at
            fallback_note = "Wczorajsze smaki (dzisiejsze wkrótce)"

        except DailySelection.DoesNotExist:
            # Ostateczny fallback: wszystkie aktywne smaki
            flavors = list(Flavor.objects.filter(status='active'))
            fallback_note = "Wszystkie dostępne smaki"

    # Sortowanie według display_order jeśli dostępne
    if flavors and 'selection' in locals() and selection.display_order:
        order_map = {pk: idx for idx, pk in enumerate(selection.display_order)}
        flavors.sort(key=lambda f: order_map.get(f.pk, 9999))

    # Przeniesienie hit_of_the_day na pierwszą pozycję
    if hit_of_the_day and hit_of_the_day in flavors:
        flavors.remove(hit_of_the_day)
        flavors.insert(0, hit_of_the_day)

    context = {
        'flavors': flavors,
        'hit_of_the_day': hit_of_the_day,
        'last_updated': last_updated,
        'fallback_note': fallback_note,
    }

    return render(request, 'flavors/homepage.html', context)
