from django.views.generic import TemplateView

class GalleryView(TemplateView):
    template_name = 'listings/gallery.html'

class ArtworkDetailView(TemplateView):
    template_name = 'listings/artwork-detail.html'

class CheckoutView(TemplateView):
    template_name = 'listings/checkout.html'


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Artwork, ArtworkImage

def gallery_view(request):
    """View for the gallery page with filtering capabilities"""
    artworks = Artwork.objects.all().order_by('-date_added')
    
    # Handle filters
    style = request.GET.get('style')
    medium = request.GET.get('medium')
    price_range = request.GET.get('price_range')
    sort = request.GET.get('sort', 'featured')
    
    if style:
        artworks = artworks.filter(style__icontains=style)
    
    if medium:
        artworks = artworks.filter(medium=medium)
    
    if price_range:
        max_price = int(price_range)
        artworks = artworks.filter(price__lte=max_price)
    
    # Handle sorting
    if sort == 'price_low':
        artworks = artworks.order_by('price')
    elif sort == 'price_high':
        artworks = artworks.order_by('-price')
    elif sort == 'newest':
        artworks = artworks.order_by('-date_added')
    elif sort == 'artist':
        artworks = artworks.order_by('artist__user__last_name')
    else:  # Default to featured
        artworks = artworks.order_by('-featured', '-date_added')
    
    # Pagination
    paginator = Paginator(artworks, 12)  # Show 12 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'artwork_count': artworks.count(),
    }
    
    return render(request, 'listings/gallery.html', context)

def artwork_detail(request, artwork_id=None, slug=None):
    """View for the artwork detail page"""
    if slug:
        artwork = get_object_or_404(Artwork, slug=slug)
    else:
        artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    # Increment view counter
    artwork.views += 1
    artwork.save()
    
    # Get related artworks (same artist or style)
    related_artworks = Artwork.objects.filter(
        Q(artist=artwork.artist) | Q(style=artwork.style)
    ).exclude(id=artwork.id)[:4]
    
    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
    }
    
    return render(request, 'listings/artwork_detail.html', context)

def checkout_view(request, artwork_id=None):
    """View for the checkout page"""
    # If artwork_id is provided, we're buying just one item
    if artwork_id:
        artwork = get_object_or_404(Artwork, pk=artwork_id)
        cart_items = [artwork]
        subtotal = artwork.price
    else:
        # In a real app, you'd get the cart items from session or database
        cart_items = []
        subtotal = 0
    
    # Calculate totals
    tax_rate = 0.08  # 8%
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_rate': tax_rate * 100,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'listings/checkout.html', context)