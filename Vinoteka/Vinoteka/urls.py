from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView

from Vinoteka import settings
from pages.views import HomepageList, NotHavenTastedList
from vine.forms import CustomUserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', HomepageList.as_view(), name='home'),
    path('new/', NotHavenTastedList.as_view(), name='new'),
    path('vine/', include('vine.urls')),
    path('auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('vine:index'),
        ),
        name='registration',
    ),
]
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
