from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from vine.forms import CommentForm, VineForm
from vine.mixins import (AuthorOrSuperUserRequiredMixin, BaseCommentmixin,
                         BaseVineMixin, SuperUserRequiredMixin)
from vine.models import Category, Comment, Vine
from Vinoteka import settings


class VineList(BaseVineMixin, ListView):
    template_name = 'vine/index.html'
    paginate_by = settings.VINE_COUNT_ON_INDEX_PAGE

    def get_queryset(self):
        return Vine.objects.filter(tasting=True).prefetch_related(
            'variety').select_related(
            'category',
            'colors',
            'sweetness'
        )


class AddVine(SuperUserRequiredMixin, BaseVineMixin, CreateView):
    form_class = VineForm
    template_name = 'vine/create.html'


class UpdateVine(SuperUserRequiredMixin, BaseVineMixin, UpdateView):
    form_class = VineForm
    pk_url_kwarg = 'vine_id'
    template_name = 'vine/create.html'


class DeleteVine(SuperUserRequiredMixin, BaseVineMixin, DeleteView):
    pk_url_kwarg = 'vine_id'
    success_url = reverse_lazy('vine:index')
    template_name = 'vine/create.html'


class VineDetail(DetailView):
    model = Vine
    template_name = 'vine/detail.html'
    pk_url_kwarg = 'vine_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vine = context['vine']
        context['comments'] = Comment.objects.filter(vine=vine)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        else:
            context['form'] = None
        context['cat_selected'] = context['object'].category_id
        return context


class VineCategory(ListView):
    model = Vine
    template_name = 'vine/category.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['category'] = category
        context['cat_selected'] = category.id
        return context

    def get_queryset(self):
        return Vine.objects.filter(category__slug=self.kwargs['cat_slug'],
                                   tasting=True).prefetch_related(
            'variety').select_related('category', 'colors', 'sweetness')


class AddComment(LoginRequiredMixin, BaseCommentmixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        vine_id = self.kwargs['vine_id']
        vine = get_object_or_404(Vine, pk=vine_id)
        form.instance.vine_id = vine.id
        return super().form_valid(form)


class UpdateComment(AuthorOrSuperUserRequiredMixin,
                    BaseCommentmixin, UpdateView):
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class DelComment(AuthorOrSuperUserRequiredMixin,
                 BaseCommentmixin, DeleteView):
    pk_url_kwarg = 'comment_id'
