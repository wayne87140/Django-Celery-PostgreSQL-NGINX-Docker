from django.urls import path
from search import views


app_name = 'search'
urlpatterns=[
    path('', views.search, name='search'),
    path('plot/<str:IPorCOM>/', views.plot, name='plot'),
    path('findplot/', views.findplot, name='findplot'),
]