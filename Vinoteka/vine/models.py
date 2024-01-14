from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class Variety(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name='Сорт'
    )

    class Meta:
        verbose_name = 'сорт винограда'
        verbose_name_plural = 'Сорта винограда'

    def __str__(self):
        return self.name[:settings.MAX_TITLE_LENGTH]


class Color(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name='Цвет напитка'
    )

    class Meta:
        verbose_name = 'цвет винограда'
        verbose_name_plural = 'Цвета винограда'

    def __str__(self):
        return self.name[:settings.MAX_TITLE_LENGTH]


class Sweetness(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name='Сладость'
    )

    class Meta:
        verbose_name = 'количество сахара'
        verbose_name_plural = 'Количество сахара'

    def __str__(self):
        return self.name[:settings.MAX_TITLE_LENGTH]


class Category(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=settings.MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='URL'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.MAX_TEXT_LENGTH]

    def get_absolute_url(self):
        return reverse('categories', kwargs={'slug:cat_slug': self.slug})


class Vine(models.Model):
    title = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name='Наименование вина'
    )
    slug = models.SlugField(
        max_length=settings.MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='URL',
        help_text='Разрешены символы латиницы, цифры, дефис и подчёркивание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='vine_cat'
    )
    colors = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Цвет',
        related_name='vine_col'
    )
    sweetness = models.ForeignKey(
        Sweetness,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Сладость',
        related_name='vine_sweet'
    )
    variety = models.ForeignKey(
        Variety,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Сорт винограда',
        related_name='vine_var'
    )
    factory = models.CharField(max_length=settings.MAX_TITLE_LENGTH, verbose_name='Завод изготовителя')
    year = models.PositiveIntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(1000, message='Введите год от 1000'),
            MaxValueValidator(3000, message='Введите год одо 3000')
        ],
        help_text='Введите год в формате YYYY (например, 2022)',
    )
    image = models.ImageField('Этикетка', upload_to='vine_images', blank=True)
    description = models.TextField(
        max_length=settings.MAX_TEXT_LENGTH,
        blank=True,
        verbose_name='Описание'
    )
    tasty = models.BooleanField(
        default=False,
        verbose_name='Вкусно!',
        help_text='Не забудь поставить галочку, если напиток тебе понравился.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Дегустатор'
    )
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'винный напиток'
        verbose_name_plural = 'Винные напитки'
        ordering = ('title',)

    def __str__(self):
        return self.title[:settings.MAX_TEXT_LENGTH]

    def get_absolute_url(self):
        return reverse('vine:show_vine', kwargs={'vine_slug': self.slug})


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vine = models.ForeignKey(
        Vine,
        on_delete=models.CASCADE,
        related_name='comments',
    )
