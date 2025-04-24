# listings/urls.py
from django.urls import path
from .views import GalleryView, ArtworkDetailView, CheckoutView

urlpatterns = [
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork_detail'),
    path('checkout/<int:pk>/', CheckoutView.as_view(), name='checkout'),
]