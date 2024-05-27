from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from vine.models import Comment, Vine

"""
Авторизированный и неавторизированный пользователи не могут создать напитки.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client',
    (pytest.lazy_fixture('client'), pytest.lazy_fixture('author_client'))
)
def test_anonymous_user_and_user_cant_create_vine(
        parametrized_client, form_vine_data):
    parametrized_client.post(reverse('vine:create_vine'), data=form_vine_data)
    assert Vine.objects.count() == 0


"""
Авторизированный пользователь не может изменять и удалять напитки.
"""


def test_user_cant_edit_vine(author_client, vine, form_vine_data):
    response = author_client.post(
        reverse('vine:edit_vine', args=(vine.id,)),
        data=form_vine_data
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    vine_from_db = Vine.objects.get(id=vine.id)
    vine.refresh_from_db()
    assert vine.title == vine_from_db.title
    assert vine.category == vine_from_db.category
    assert vine.colors == vine_from_db.colors
    assert vine.sweetness == vine_from_db.sweetness
    assert vine.factory == vine_from_db.factory
    assert vine.year == vine_from_db.year
    assert vine.description == vine_from_db.description


def test_user_cant_delete_vine(author_client, vine):
    response = author_client.delete(
        reverse('vine:delete_vine', args=(vine.id,)))
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert Vine.objects.count() == 1


"""
Неавторизованный пользователь не может создавать комментарии.
"""


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, vine):
    url = reverse('vine:create_comment', args=(vine.id,))
    response = client.post(url, {'text': 'New comment text'})
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


"""
Авторизованный пользователь может отправлять комментарии.
"""


def test_user_can_create_comment(
        author_client, vine, author, form_comment_data):
    url = reverse('vine:create_comment', args=(vine.id,))
    response = author_client.post(url, form_comment_data)
    assertRedirects(response, reverse('vine:show_vine', args=(vine.id,)))
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_comment_data['text']
    assert comment.vine == form_comment_data['vine']
    assert comment.author == author


"""
Авторизованный пользователь может изменять и удалять свои комментарии.
"""


def test_author_can_edit_comment(
        author_client, comment, vine, form_comment_data):
    url = reverse(
        'vine:edit_comment',
        kwargs={'vine_id': vine.id, 'comment_id': comment.id}
    )
    response = author_client.post(url, form_comment_data)
    assertRedirects(response, reverse('vine:show_vine', args=(vine.id,)))
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.text == form_comment_data['text']


def test_author_can_delete_comment(author_client, vine, comment):
    response = author_client.delete(
        reverse('vine:delete_comment',
                kwargs={'vine_id': vine.id, 'comment_id': comment.id}))
    assertRedirects(response, reverse('vine:show_vine', args=(vine.id,)))
    assert Comment.objects.count() == 0


"""
Авторизованный пользователь не может изменять и удалять чужие комментарии.
"""


def test_other_user_cant_edit_comment(
        not_author_client, vine_id, comment_id, form_comment_data, comment):
    response = not_author_client.post(reverse(
        'vine:edit_comment',
        kwargs={'vine_id': vine_id, 'comment_id': comment_id}),
        form_comment_data
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    comment_from_db = Comment.objects.get(id=comment_id)
    assert comment.text == comment_from_db.text


def test_other_user_cant_delete_comment(
        not_author_client, vine_id, comment_id, comment):
    response = not_author_client.delete(reverse(
        'vine:delete_comment',
        kwargs={'vine_id': vine_id, 'comment_id': comment_id})
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert Comment.objects.count() == 1


"""
Суперюзер может изменять и удалять чужие комментарии.
"""


def test_admin_can_edit_comment(admin, comment, vine, form_comment_data):
    url = reverse(
        'vine:edit_comment',
        kwargs={'vine_id': vine.id, 'comment_id': comment.id}
    )
    response = admin.post(url, form_comment_data)
    assertRedirects(response, reverse('vine:show_vine', args=(vine.id,)))
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.text == form_comment_data['text']


def test_admin_can_delete_comment(admin, vine, comment):
    response = admin.delete(
        reverse('vine:delete_comment',
                kwargs={'vine_id': vine.id, 'comment_id': comment.id}))
    assertRedirects(response, reverse('vine:show_vine', args=(vine.id,)))
    assert Comment.objects.count() == 0
