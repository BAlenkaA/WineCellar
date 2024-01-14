from django import forms
from datetime import datetime

from django.core.exceptions import ValidationError

from .models import Comment, Vine


class VineForm(forms.ModelForm):
    class Meta:
        model = Vine
        fields = (
            'title',
            'slug',
            'category',
            'colors',
            'sweetness',
            'variety',
            'year',
            'factory',
            'image',
            'description',
            'tasty'
        )

    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = datetime.now().year
        if year > current_year:
            raise ValidationError('Год производства вина не может быть больше текущего')
        return year


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
