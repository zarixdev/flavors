import logging
import uuid
import os
from datetime import datetime
from io import BytesIO

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image

logger = logging.getLogger(__name__)

PREDEFINED_TAGS = {
    'vegan': {'label': 'Wegański', 'color': 'green'},
    'lactose-free': {'label': 'Bez laktozy', 'color': 'blue'},
    'new': {'label': 'Nowość', 'color': 'purple'},
    'hit': {'label': 'Hit dnia', 'color': 'red'},
    'sugar-free': {'label': 'Bez cukru', 'color': 'yellow'},
    'seasonal': {'label': 'Sezonowy', 'color': 'orange'},
}


def uuid_upload_to(instance, filename):
    """Generate UUID-based filename for collision-free storage."""
    ext = 'webp'  # Force WebP since we convert in save()
    date_path = datetime.now().strftime('%Y/%m')
    return f'flavors/{date_path}/{uuid.uuid4().hex}.{ext}'


class Flavor(models.Model):
    FLAVOR_TYPES = [
        ('milk', 'Mleczny'),
        ('sorbet', 'Sorbet'),
    ]

    STATUS_CHOICES = [
        ('active', 'Aktywny'),
        ('archived', 'Zarchiwizowany'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    description = models.TextField(blank=True)
    flavor_type = models.CharField(max_length=20, choices=FLAVOR_TYPES, default='milk')
    tags = models.JSONField(default=list, blank=True)
    is_seasonal = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=uuid_upload_to, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 2
            while Flavor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Process image only if it's new or changed
        if self.photo and hasattr(self.photo, 'file'):
            # Check if photo is new or changed
            is_new_photo = False
            if self.pk is None:
                # New object - always process
                is_new_photo = True
            else:
                # Existing object - check if photo changed
                try:
                    existing = self.__class__.objects.filter(pk=self.pk).first()
                    if existing is None or existing.photo.name != self.photo.name:
                        is_new_photo = True
                except Exception:
                    # If check fails, assume it's new/changed to be safe
                    is_new_photo = True

            if is_new_photo:
                try:
                    img = Image.open(self.photo)

                    if img.mode == 'P':
                        img = img.convert('RGBA')

                    # Resize to max 1200px maintaining aspect ratio
                    max_size = (1200, 1200)
                    img.thumbnail(max_size, Image.BICUBIC)

                    # Save as WebP with 85% quality
                    buffer = BytesIO()
                    img.save(buffer, format='WEBP', quality=85)

                    # Replace file content with optimized version
                    file_content = ContentFile(buffer.getvalue())
                    # uuid_upload_to generates the actual filename with UUID
                    self.photo.save('temp.webp', file_content, save=False)
                except Exception as e:
                    # If image processing fails, log and continue with original
                    logger.warning(f"Image processing failed for {self.name}: {e}")

        super().save(*args, **kwargs)

    def clean(self):
        if len(self.tags) > 5:
            raise ValidationError({'tags': 'Możesz wybrać maksymalnie 5 tagów.'})

    def __str__(self):
        return self.name


class DailySelection(models.Model):
    date = models.DateField(unique=True)
    flavors = models.ManyToManyField(Flavor, blank=True)
    hit_of_the_day = models.ForeignKey(
        Flavor,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='hit_days'
    )
    display_order = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dzisiejsze smaki: {self.date}"

    def get_ordered_flavors(self):
        """
        Return flavors in display_order, with any unlisted flavors appended at end.
        Uses order_map for efficient sorting.
        """
        all_flavors = list(self.flavors.all())
        if not all_flavors:
            return []

        # Build order mapping: flavor_id -> position in display_order
        order_map = {fid: idx for idx, fid in enumerate(self.display_order or [])}

        # Sort: flavors in display_order by their position, then unlisted flavors at end
        def sort_key(flavor):
            if flavor.id in order_map:
                return (0, order_map[flavor.id])
            return (1, 0)  # Unlisted flavors come after

        return sorted(all_flavors, key=sort_key)

    def add_flavor_to_order(self, flavor_id):
        """
        Append flavor ID to display_order if not already present.
        Call this when adding a flavor to the selection.
        """
        if self.display_order is None:
            self.display_order = []

        if flavor_id not in self.display_order:
            self.display_order.append(flavor_id)
            self.save(update_fields=['display_order'])

    def remove_flavor_from_order(self, flavor_id):
        """
        Remove flavor ID from display_order if present.
        Call this when removing a flavor from the selection.
        """
        if self.display_order and flavor_id in self.display_order:
            self.display_order = [fid for fid in self.display_order if fid != flavor_id]
            self.save(update_fields=['display_order'])

    def move_flavor(self, flavor_id, direction):
        """
        Move flavor up or down in display_order.
        direction: -1 for up (earlier), +1 for down (later)
        Returns True if move was successful, False otherwise.
        """
        if not self.display_order or flavor_id not in self.display_order:
            return False

        current_index = self.display_order.index(flavor_id)
        new_index = current_index + direction

        # Validate boundary conditions
        if new_index < 0 or new_index >= len(self.display_order):
            return False

        # Swap positions
        self.display_order[current_index], self.display_order[new_index] = \
            self.display_order[new_index], self.display_order[current_index]

        self.save(update_fields=['display_order'])
        return True
