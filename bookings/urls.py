from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reserve/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('confirmation/<int:reservation_id>/', views.confirmation, name='confirmation'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu, name='menu'),
]