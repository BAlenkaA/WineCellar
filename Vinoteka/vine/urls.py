from django.urls import path

from .views import index, add_vine, show_vine, show_category, delete_vine

app_name = 'vine'

urlpatterns = [
    path('', index, name='index'),
    path('categories/<slug:cat_slug>/', show_category, name='categories'),
    path('add_vine/', add_vine, name='create_vine'),
    path('<slug:vine_slug>/', show_vine, name='show_vine'),
    path('<slug:vine_slug>/edit/', add_vine, name='edit_vine'),
    path('<slug:vine_slug>/delete/', delete_vine, name='delete_vine'),
]
