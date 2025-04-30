# listings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path('artwork/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('artwork/<slug:slug>/', views.artwork_detail, name='artwork_detail_slug'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/review/', views.checkout_review, name='checkout_review'),
    path('checkout/<int:artwork_id>/', views.checkout_view, name='checkout_with_artwork'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/confirmation/', views.checkout_confirmation, name='checkout_confirmation'),
]