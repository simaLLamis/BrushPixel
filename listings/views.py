from django.views.generic import TemplateView

class GalleryView(TemplateView):
    template_name = 'listings/gallery.html'

class ArtworkDetailView(TemplateView):
    template_name = 'listings/artwork-detail.html'

class CheckoutView(TemplateView):
    template_name = 'listings/checkout.html'