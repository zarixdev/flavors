from django import forms
from django.core.exceptions import ValidationError
import json
from .models import Flavor


class FlavorForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Flavor
        fields = ['name', 'photo', 'description', 'flavor_type', 'tags', 'is_seasonal']

    def clean_tags(self):
        tags_json = self.cleaned_data.get('tags', '[]')
        try:
            tags = json.loads(tags_json) if tags_json else []
        except json.JSONDecodeError:
            raise ValidationError('Nieprawidłowy format tagów')

        if not isinstance(tags, list):
            raise ValidationError('Tagi muszą być listą')

        if len(tags) > 5:
            raise ValidationError('Możesz wybrać maksymalnie 5 tagów')

        return tags
