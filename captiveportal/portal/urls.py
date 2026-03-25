from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('success', views.success, name='success'),
    path('logout', views.logout, name='logout'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)