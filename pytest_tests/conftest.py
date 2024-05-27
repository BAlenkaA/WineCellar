import pytest
from django.test.client import Client
from vine.models import Category, Color, Comment, Sweetness, Variety, Vine

from Vinoteka import settings


@pytest.fixture
def category():
    return Category.objects.create(name='Вино', slug='vino')


@pytest.fixture
def color():
    return Color.objects.create(name='Красное')


@pytest.fixture
def sweetness():
    return Sweetness.objects.create(name='Сладкое')


@pytest.fixture
def variety():
    return [Variety.objects.create(name=name) for name in [
        'Ркацители', 'Мерло']]


@pytest.fixture
def vine(category, color, sweetness, variety):
    vine = Vine.objects.create(
        title='Название',
        category=category,
        colors=color,
        sweetness=sweetness,
        factory='Фотисаль',
        year=2020,
        description='Какое-то описание'
    )
    vine.variety.add(*variety)
    return vine


@pytest.fixture
def vine_index_list(admin_user, color, sweetness, category):
    return Vine.objects.bulk_create(
        Vine(
            title=f'Название вина {index}',
            category=category,
            colors=color,
            sweetness=sweetness,
            factory=f'Завод {index}',
            year=f'200{index}',
            description='Просто какое-то описание.',
            )
        for index in range(settings.VINE_COUNT_ON_INDEX_PAGE)
    )


@pytest.fixture
def form_vine_data(category, color, sweetness):
    return {
        'title': 'Очередное вмно',
        'category': category,
        'colors': color,
        'sweetness': sweetness,
        'factory': 'Какой-то заваод',
        'year': 2000,
        'description': 'Просто какое-то описание вина.',
    }


@pytest.fixture
def admin(admin_user):
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор комментария')


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def vine_id(vine):
    return vine.id


@pytest.fixture
def cat_slug(category):
    return category.slug


@pytest.fixture
def comment(vine, author):
    comment = Comment.objects.create(
        text='Какой-то текст комментария',
        author=author,
        vine=vine
    )
    return comment


@pytest.fixture
def form_comment_data(vine, author):
    return {
        'text': 'Какой-то новый текст комментария',
        'author': author,
        'vine': vine
    }


@pytest.fixture
def comment_id(comment):
    return comment.id
