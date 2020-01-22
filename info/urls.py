from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'info'
urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('confirmation/', views.visit_confirm, name='confirm'),
]

urlpatterns += staticfiles_urlpatterns()