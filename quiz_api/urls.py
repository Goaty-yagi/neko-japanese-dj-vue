from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/',include('enquire.urls')),
    path('api/',include('quiz.urls')),
    path('api/',include('user.urls')),
    path('api/',include('log.urls')),
    path('api/',include('notification.urls')),
    path('api/board/',include('board.urls')),
    path('api/',include('message.urls')),
    path('api/auth/',include('dj_rest_auth.urls')),
    path('api/auth/registration/',include('dj_rest_auth.registration.urls')),
    re_path('.*', TemplateView.as_view(template_name='index.html'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns