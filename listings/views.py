from django.views.generic import TemplateView
class GalleryView(TemplateView):
    template_name = 'listings/gallery.html'

class ArtworkDetailView(TemplateView):
    template_name = 'listings/artwork-detail.html'

class CheckoutView(TemplateView):
    template_name = 'listings/checkout.html'


from django.shortcuts import render, get_object_or_404,redirect
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
    for artwork in cart_items:
        artwork.display_image = artwork.images.filter(is_primary=True).first() or artwork.images.first()
    from decimal import Decimal
    # Calculate totals
    tax_rate = 0.08  # 8%
    tax = subtotal * Decimal(str(tax_rate))
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_rate': tax_rate * 100,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'listings/checkout.html', context)
def checkout_review(request):
    """
    View for the checkout review page.
    """
    # Get cart items from session
    cart_items = []
    subtotal = 0
    
    # If you're storing cart items as artwork IDs in the session
    cart = request.session.get('cart', {})
    
    # If you have a Cart model, you might use something like:
    # if request.user.is_authenticated:
    #     cart_items = CartItem.objects.filter(user=request.user)
    # else:
    #     cart_items = []
    
    # For the session-based approach, get the artwork objects
    if cart:
        from .models import Artwork  # Import your Artwork model
        
        for artwork_id, quantity in cart.items():
            try:
                artwork = Artwork.objects.get(id=artwork_id)
                cart_items.append(artwork)
                subtotal += artwork.price
            except Artwork.DoesNotExist:
                pass
    
    # Alternatively, if you already have cart items in your session:
    # cart_items = request.session.get('cart_items', [])
    # subtotal = request.session.get('subtotal', 0)
    
    # Calculate tax and total
    tax_rate = 8.5  # Example tax rate
    tax = subtotal * tax_rate / 100
    total = subtotal + tax
    
    # Get billing info from session
    billing = {
        'first_name': request.session.get('billing_first_name', ''),
        'last_name': request.session.get('billing_last_name', ''),
        'email': request.session.get('billing_email', ''),
        'phone': request.session.get('billing_phone', ''),
        'address': request.session.get('billing_address', ''),
        'city': request.session.get('billing_city', ''),
        'state': request.session.get('billing_state', ''),
        'postcode': request.session.get('billing_postcode', ''),
        'country': request.session.get('billing_country', ''),
    }
    
    # Get payment method info from session
    payment_method = request.session.get('payment_method', 'credit_card')
    
    # Additional payment details
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total,
        'billing': billing,
        'payment_method': payment_method,
    }
    
    # Add payment method specific details
    if payment_method == 'credit_card':
        context['last_four'] = request.session.get('card_last_four', 'XXXX')
        context['expiry_date'] = request.session.get('card_expiry', 'XX/XX')
    elif payment_method == 'paypal':
        context['paypal_email'] = request.session.get('paypal_email', '')
    
    return render(request, 'listings/checkout_review.html', context)
def checkout_payment(request):
    """
    View for the checkout payment page.
    If the form is submitted, it processes the payment information
    and redirects to the review page.
    """
    # Get cart items - using the same approach as in checkout_review
    cart_items = []
    subtotal = 0
    
    # If you're storing cart items as artwork IDs in the session
    cart = request.session.get('cart', {})
    
    if cart:
        from .models import Artwork  # Import your Artwork model
        
        for artwork_id, quantity in cart.items():
            try:
                artwork = Artwork.objects.get(id=artwork_id)
                cart_items.append(artwork)
                subtotal += artwork.price
            except Artwork.DoesNotExist:
                pass
    
    # Calculate tax and total
    tax_rate = 8.5  # Example tax rate
    tax = subtotal * tax_rate / 100
    total = subtotal + tax
    
    # Process form submission
    if request.method == 'POST':
        # Save billing information to session
        request.session['billing_first_name'] = request.POST.get('firstName', '')
        request.session['billing_last_name'] = request.POST.get('lastName', '')
        request.session['billing_email'] = request.POST.get('email', '')
        request.session['billing_phone'] = request.POST.get('phone', '')
        request.session['billing_address'] = request.POST.get('address', '')
        request.session['billing_city'] = request.POST.get('city', '')
        request.session['billing_state'] = request.POST.get('state', '')
        request.session['billing_postcode'] = request.POST.get('postcode', '')
        request.session['billing_country'] = request.POST.get('country', '')
        
        # Save payment method to session
        payment_method = request.POST.get('paymentMethod', 'credit_card')
        request.session['payment_method'] = payment_method
        
        # Save payment details based on method
        if payment_method == 'credit_card':
            card_number = request.POST.get('cardNumber', '')
            if card_number:
                # Store only the last 4 digits for security
                request.session['card_last_four'] = card_number.replace(' ', '')[-4:]
            
            request.session['card_expiry'] = request.POST.get('expiryDate', '')
        elif payment_method == 'paypal':
            request.session['paypal_email'] = request.POST.get('paypalEmail', '')
        
        # Redirect to review page
        return redirect('checkout_review')
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'listings/checkout_payment.html', context)
def checkout_confirmation(request):
    """
    View for the checkout confirmation page.
    This is displayed after successful order processing.
    """
    # In a real application, you would process the order here
    # For example:
    # 1. Create an Order object in the database
    # 2. Process payment through payment gateway
    # 3. Send confirmation email
    # 4. Clear the cart
    
    # Generate a random order number for demonstration
    import random
    import string
    order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Get the cart items
    cart_items = []
    subtotal = 0
    
    # If you're storing cart items as artwork IDs in the session
    cart = request.session.get('cart', {})
    
    if cart:
        from .models import Artwork  # Import your Artwork model
        
        for artwork_id, quantity in cart.items():
            try:
                artwork = Artwork.objects.get(id=artwork_id)
                cart_items.append(artwork)
                subtotal += artwork.price
            except Artwork.DoesNotExist:
                pass
    
    # Calculate tax and total
    tax_rate = 8.5  # Example tax rate
    tax = subtotal * tax_rate / 100
    total = subtotal + tax
    
    # Get billing information
    billing = {
        'first_name': request.session.get('billing_first_name', ''),
        'last_name': request.session.get('billing_last_name', ''),
        'email': request.session.get('billing_email', ''),
    }
    
    # In a real application, you would clear the cart after successful checkout
    # For demonstration, we'll leave it in the session
    
    context = {
        'order_number': order_number,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'billing': billing,
    }
    
    return render(request, 'listings/checkout_confirmation.html', context)