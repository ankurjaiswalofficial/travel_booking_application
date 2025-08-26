from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('travel/', views.travel_list, name='travel_list'),
    path('book/<str:travel_id>/', views.book_travel, name='book_travel'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<str:booking_id>/cancel/',
         views.cancel_booking, name='cancel_booking'),
]
