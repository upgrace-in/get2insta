from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from get2i import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('mail_us/', views.mail_us, name='mail_us'),
    path('about_us/', TemplateView.as_view(template_name='get2i/about_us.html'), name='about_us'),
    path('packages/', TemplateView.as_view(template_name='get2i/get_in_bulk.html'), name='bulk'),
    path('how_it_works/', TemplateView.as_view(template_name='get2i/how_it_works.html'), name='how_it_works'),
    path('', TemplateView.as_view(template_name='get2i/index.html'), name='index'),
    path('follow_count/', views.flw_count, name='follow_count'),
    path('bot/', views.Insta_Bot.as_view(), name='bot'),


    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
