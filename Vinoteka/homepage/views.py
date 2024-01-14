from django.http import HttpResponse
from django.shortcuts import render

from vine.models import Vine, Category


# Create your views here.
def homepage(request):
    vines = Vine.objects.all()
    context = {
        'vines': vines,
        'cat_selected': 0
    }
    return render(request, 'homepage/tasty_list.html', context=context)
