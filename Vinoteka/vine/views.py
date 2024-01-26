from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from vine.forms import VineForm, CommentForm
from vine.models import Vine, Category, Comment


class VineList(ListView):
    model = Vine
    template_name = 'vine/index.html'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Vine.objects.filter(tasting=True).prefetch_related('variety').select_related(
            'category',
            'colors',
            'sweetness',
            'author'
        )


class AddVine(LoginRequiredMixin, CreateView):
    model = Vine
    form_class = VineForm
    template_name = 'vine/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateVine(LoginRequiredMixin, UpdateView):
    model = Vine
    form_class = VineForm
    template_name = 'vine/create.html'
    pk_url_kwarg = 'vine_id'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context


class DeleteVine(LoginRequiredMixin, DeleteView):
    model = Vine
    template_name = 'vine/create.html'
    pk_url_kwarg = 'vine_id'
    success_url = reverse_lazy('vine:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        form = VineForm(instance=instance)
        context['form'] = form
        context['cat_selected'] = 0
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class VineDetail(DetailView):
    model = Vine
    template_name = 'vine/detail.html'
    pk_url_kwarg = 'vine_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vine = context['vine']
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(vine=vine).select_related('author')
        context['cat_selected'] = context['object'].category_id
        return context

    def get_queryset(self):
        return Vine.objects.filter(tasting=True).prefetch_related('variety').select_related(
            'category',
            'colors',
            'sweetness',
            'author'
        )


class VineCategory(ListView):
    model = Vine
    template_name = 'vine/category.html'
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['category'] = category
        context['cat_selected'] = category.id
        return context

    def get_queryset(self):
        return Vine.objects.filter(category__slug=self.kwargs['cat_slug'], tasting=True).prefetch_related(
            'variety').select_related('category', 'colors', 'sweetness')


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'vine/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        vine_id = self.kwargs['vine_id']
        vine = get_object_or_404(Vine, pk=vine_id)
        form.instance.vine_id = vine.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'vine:show_vine',
            kwargs={'vine_id': self.kwargs['vine_id']})


class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'vine/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'vine:show_vine',
            kwargs={'vine_id': self.kwargs['vine_id']})


class DelComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'vine/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'vine:show_vine',
            kwargs={'vine_id': self.kwargs['vine_id']})


# Далее предполагается работа над API и подключение телеграмм-бота
