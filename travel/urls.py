from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('destination/', views.destination, name='destination'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('destination/<int:pk>/things-to-explore/', views.things_to_explore, name='things_to_explore'),
    path('destination/<int:pk>/famous-restaurants/', views.famous_restaurants, name='famous_restaurants'),
    path('destination/<int:pk>/must-visit-places/', views.must_visit_places, name='must_visit_places'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),
    path('book/<int:pk>/', views.book_destination, name='book_destination'),
    path('send_confirmation_email/<int:booking_id>/', views.send_confirmation_email, name='send_confirmation_email'),
    path('payment/confirmation/<int:booking_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('password_reset/', views.PasswordResetView.as_view(template_name='forgot_password.html'), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]


