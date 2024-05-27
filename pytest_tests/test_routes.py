from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

"""
Для всех пользователей доступны страницы логина, логаута и регистрации.
А также главная страница, страница винотеки, страница не дегустированного.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('login', 'logout', 'registration', 'home', 'vine:index', 'new')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


"""
Всем пользователям доступна страница деталей вина, страницы категорий.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('vine:show_vine', pytest.lazy_fixture('vine_id')),
        ('vine:categories', pytest.lazy_fixture('cat_slug'))
    )
)
def test_parameter_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=(args,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


"""
Только суперпользователю доступна страница создания вина.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin'), HTTPStatus.OK),
        (pytest.lazy_fixture('author_client'), HTTPStatus.FORBIDDEN),
    ),
)
def test_creation_page_vine_availability(
        vine, parametrized_client, expected_status
):
    url = reverse('vine:create_vine')
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


"""
Только суперюзеру доступны страницы редактирования и удаления вина.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin'), HTTPStatus.OK),
        (pytest.lazy_fixture('author_client'), HTTPStatus.FORBIDDEN),
    ),
)
@pytest.mark.parametrize(
    'name',
    ('vine:edit_vine', 'vine:delete_vine'),
)
def test_add_pages_availability_for_different_users(
        name, parametrized_client, expected_status, vine_id
):
    url = reverse(name, args=(vine_id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


"""
Автор и суперюзер имеют доступ к редактированию/удалению комментов.
Анонимный пользоватеть - нет.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin'), HTTPStatus.OK),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'),  HTTPStatus.FORBIDDEN),
    )
)
@pytest.mark.parametrize(
    'name',
    ('vine:edit_comment', 'vine:delete_comment')
)
def test_creation_page_comment_availability(
        name, comment_id, vine_id, parametrized_client, expected_status
):
    url = reverse(name, kwargs={'vine_id': vine_id, 'comment_id': comment_id})
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


"""
Аноним перенаправляеться на страницу логина при добавлении/измении вина.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('vine:edit_vine', pytest.lazy_fixture('vine_id')),
        ('vine:delete_vine', pytest.lazy_fixture('vine_id')),
        ('vine:create_vine', None)
    ),
)
def test_vine_redirects_not_logged_in(client, name, args):
    login_url = reverse('login')
    if args:
        url = reverse(name, args=(args,))
    else:
        url = reverse(name)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


"""
Аноним перенаправляеться на страницу логина при добавлении коммента.
"""


@pytest.mark.django_db
def test_add_comment_redirect_if_not_logged_in(client, vine_id):
    login_url = reverse('login')
    url = reverse('vine:create_comment', args=(vine_id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


"""
Аноним перенаправляеться на страницу логина при изменении/удалении комментов.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('vine:edit_comment', 'vine:delete_comment'),
)
def test_update_or_destroy_comment_redirect_if_not_logged_in(
        client, name, vine_id, comment_id):
    login_url = reverse('login')
    url = reverse(name, kwargs={'vine_id': vine_id, 'comment_id': comment_id})
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
