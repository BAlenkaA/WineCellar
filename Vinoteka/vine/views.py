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


def add_vine(request, vine_slug=None):
    if vine_slug is not None:
        instance = get_object_or_404(Vine, slug=vine_slug)
    else:
        instance = None
    form = VineForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'vine/create.html', context=context)


def delete_vine(request, vine_slug):
    instance = get_object_or_404(Vine, slug=vine_slug)
    form = VineForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('vine:index')
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
