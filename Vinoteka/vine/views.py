from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from vine.forms import VineForm
from vine.models import Vine, Category


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def index(request):
    vines = Vine.objects.all()
    context = {
        'vines': vines,
        'cat_selected': 0
    }
    return render(request, 'vine/index.html', context=context)


def add_vine(request):
    if request.method == 'POST':
        form = VineForm(request.POST, request.FILES)
        if form.is_valid():
            vine = form.save(commit=False)
            vine.author = request.user
            vine.save()
            return redirect('home')
    else:
        form = VineForm
    context = {
        'form': form
    }
    return render(request, 'vine/create.html', context=context)


def show_vine(request, vine_slug):
    vine = get_object_or_404(Vine, slug=vine_slug)
    context = {
        'vine': vine,
        'title': vine.title,
        'cat_selected': vine.category_id
    }
    return render(request, 'vine/detail.html', context=context)


def show_category(request, cat_slug):
    category = Category.objects.get(slug=cat_slug)
    vines = Vine.objects.filter(category=category)
    context = {
        'vines': vines,
        'category': category,
        'cat_selected': category.id
    }
    return render(request, 'vine/category.html', context=context)
