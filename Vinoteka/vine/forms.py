from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, User, Vine


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class VineForm(forms.ModelForm):
    year = forms.IntegerField(
        label='Год',
        required=False,
        widget=forms.NumberInput(
            attrs={'min': 1000, 'max': datetime.now().year})
    )

    class Meta:
        model = Vine
        fields = (
            'title',
            'category',
            'colors',
            'sweetness',
            'variety',
            'year',
            'factory',
            'image',
            'description',
            'tasty',
            'tasting'
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
