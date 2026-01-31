from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
import os
from datetime import datetime

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
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    flavor_type = models.CharField(max_length=20, choices=FLAVOR_TYPES, default='milk')
    tags = models.JSONField(default=list, blank=True)
    is_seasonal = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=uuid_upload_to, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Process image if new photo uploaded
        if self.photo and hasattr(self.photo, 'file'):
            try:
                img = Image.open(self.photo)

                # Convert RGBA/P to RGB for WebP compatibility
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # Resize to max 1200px maintaining aspect ratio
                max_size = (1200, 1200)
                img.thumbnail(max_size, Image.BICUBIC)

                # Save as WebP with 85% quality
                buffer = BytesIO()
                img.save(buffer, format='WEBP', quality=85)

                # Replace file content with optimized version
                file_content = ContentFile(buffer.getvalue())
                filename = f'{uuid.uuid4().hex}.webp'
                self.photo.save(filename, file_content, save=False)
            except Exception:
                # If image processing fails, continue with original
                pass

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

    def __str__(self):
        return f"Dzisiejsze smaki: {self.date}"
