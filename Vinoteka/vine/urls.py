from django.urls import path

from .views import (
    VineList,
    VineCategory,
    VineDetail,
    AddVine,
    UpdateVine,
    DeleteVine,
    AddComment,
    UpdateComment,
    DelComment
)

app_name = 'vine'

urlpatterns = [
    path('', VineList.as_view(), name='index'),
    path('categories/<slug:cat_slug>/', VineCategory.as_view(), name='categories'),
    path('add_vine/', AddVine.as_view(), name='create_vine'),
    path('<int:vine_id>/', VineDetail.as_view(), name='show_vine'),
    path('<int:vine_id>/edit/', UpdateVine.as_view(), name='edit_vine'),
    path('<int:vine_id>/delete/', DeleteVine.as_view(), name='delete_vine'),
    path('<int:vine_id>/comment/', AddComment.as_view(), name='create_comment'),
    path('<int:vine_id>/edit_comment/<int:comment_id>/', UpdateComment.as_view(), name='edit_comment'),
    path('<int:vine_id>/delete_comment/<int:comment_id>/', DelComment.as_view(), name='delete_comment'),
]
