from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import IndexPageView, ChangeLanguageView, UserInputPageView
from accounts.views import submit_form

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', UserInputPageView.as_view(), name='index'),
    path('chat/', IndexPageView.as_view(), name='chat'),
    path('submit-form/', submit_form, name='submit_form'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
