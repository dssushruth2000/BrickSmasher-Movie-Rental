from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account_creation, name='account_creation'),
    path('movie/', views.manage_movies, name='manage_movies'),
    path('rent/', views.rent_return_movies, name='rent_return_movies'),
    path('dbRent/', views.manage_rentals, name='manage_rentals'),
]



