from django.urls import path

from cities.views import *

app_name = 'cities'

urlpatterns = [
    # path('', home_view, name='home'),
    path('', CityListView.as_view(), name='home'),
    path('add/', CityCreatelView.as_view(), name='create'),
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
]
