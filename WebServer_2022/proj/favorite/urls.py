from django.urls import path
from favorite import views



app_name = 'favorite'
urlpatterns = [
    path('', views.favorite, name='favorite'),
    path('settings/', views.settings, name='settings'),
]