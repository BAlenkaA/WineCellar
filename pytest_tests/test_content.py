from http import HTTPStatus
from math import ceil

import pytest
from django.urls import reverse
from vine.forms import CommentForm, VineForm
from vine.models import Comment, Vine

"""
На странице напитков присутствуют элементы контекста, пагинация.
Список напитков выводится согласно ожиданиям.
"""


@pytest.mark.django_db
def test_vine_list_context(client):
    url = reverse('vine:index')
    response = client.get(url)
    assert 'cat_selected' in response.context
    assert response.context['cat_selected'] == 0


def test_vine_list_pagination(client, vine_index_list):
    url = reverse('vine:index')
    response = client.get(url)
    assert response.status_code == 200
    vines_in_context = response.context['object_list']
    assert all(vine.tasting for vine in vines_in_context)
    total_vines = Vine.objects.filter(tasting=True).count()
    paginator = response.context['paginator']
    assert len(vines_in_context) == min(paginator.per_page, total_vines)
    num_pages = ceil(total_vines / paginator.per_page)
    assert paginator.num_pages == num_pages


"""
На странице напитка присутствуют элементы контекста.
Выводится список комментариев.
"""


@pytest.mark.django_db
def test_vine_detail_context(client, vine, vine_id):
    url = reverse('vine:show_vine', args=(vine_id,))
    response = client.get(url)
    assert 'vine' in response.context
    assert 'comments' in response.context
    assert list(response.context['comments']) == list(
        Comment.objects.filter(vine=vine))
    assert 'cat_selected' in response.context
    assert response.context['cat_selected'] == vine.category.id


"""
Аутентифицированный пользователь имеет доступ к форме создания комментария.
Анонимный пользователь не имеет доступ к форме создания комментария.
"""


def test_vine_detail_form_context(client, not_author_client, vine, vine_id):
    url = reverse('vine:show_vine', args=(vine_id,))
    response = client.get(url)
    assert 'form' not in response.context or response.context['form'] is None
    response = not_author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


"""
На страницах категорий присутсвтуют элементы контекста.
Присутствует пагинация, список напитков выводится согласно ожиданиям.
"""


@pytest.mark.django_db
def test_vine_category_context(client, cat_slug, category):
    url = reverse('vine:categories', args=(cat_slug,))
    response = client.get(url)
    assert 'category' in response.context
    assert response.context['category'] == category
    assert 'cat_selected' in response.context
    assert response.context['cat_selected'] == category.id


@pytest.mark.django_db
def test_vine_category_pagination(client, cat_slug, vine_index_list):
    url = reverse('vine:categories', args=(cat_slug,))
    response = client.get(url)
    assert response.status_code == 200
    vines_in_context = response.context['object_list']
    assert all(vine.tasting for vine in vines_in_context)
    total_vines = Vine.objects.filter(tasting=True).count()
    paginator = response.context['paginator']
    assert len(vines_in_context) == min(paginator.per_page, total_vines)
    num_pages = ceil(total_vines / paginator.per_page)
    assert paginator.num_pages == num_pages


"""
На странице добавления напика присутсвтуют элементы контекста.
Есть доступ к форме.
"""


def test_add_vine_context(admin_client,):
    url = reverse('vine:create_vine')
    response = admin_client.get(url)
    assert 'cat_selected' in response.context
    assert response.context['cat_selected'] == 0
    assert 'form' in response.context and isinstance(
        response.context['form'], VineForm)


"""
На странице изменения напика присутсвтуют элементы контекста.
Есть доступ к форме.
"""


def test_update_vine_context(admin_client, vine, vine_id):
    url = reverse('vine:edit_vine', args=(vine_id,))
    response = admin_client.get(url)
    assert 'cat_selected' in response.context
    assert response.context['cat_selected'] == 0
    assert 'form' in response.context
    assert response.context['form'].instance == vine


"""
При создании комментария форма правильно валидируется.
После успешного создания пользователь редиректится на страницу напитка.
"""


def test_create_comment(author_client, author, vine_id):
    url = reverse('vine:create_comment', args=(vine_id,))
    response = author_client.post(url, {'text': 'New comment text'})
    assert response.status_code == HTTPStatus.FOUND
    new_comment = Comment.objects.filter(
        vine_id=vine_id, author=author, text='New comment text')
    assert new_comment.exists()
    assert response['Location'] == reverse(
        'vine:show_vine', kwargs={'vine_id': vine_id})
