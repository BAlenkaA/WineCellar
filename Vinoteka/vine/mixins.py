from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from vine.models import Comment, Vine


class SuperUserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AuthorOrSuperUserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if request.user.is_superuser or instance.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class BaseVineMixin:
    model = Vine

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context


class BaseCommentmixin:
    model = Comment
    template_name = 'vine/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'vine:show_vine',
            kwargs={'vine_id': self.kwargs['vine_id']})
