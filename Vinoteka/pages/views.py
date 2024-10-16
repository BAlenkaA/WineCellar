from django.shortcuts import render
from django.views.generic import ListView

from vine.filters import VineFilter
from vine.models import Vine


class HomepageList(ListView):
    model = Vine
    template_name = 'pages/tasty_list.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()
        context['cat_selected'] = 0
        context['filter'] = VineFilter(self.request.GET, queryset=self.get_queryset())
        context['no_results'] = not filtered_qs.exists()
        return context

    def get_queryset(self):
        query = Vine.objects.filter(tasting=True).prefetch_related('variety').select_related(
            'category', 'colors', 'sweetness')
        filter = VineFilter(self.request.GET, queryset=query)
        return filter.qs.distinct()


class NotHavenTastedList(ListView):
    model = Vine
    template_name = 'pages/not_heven_tasted.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Vine.objects.filter(tasting=False)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403, context={'reason': reason})


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
