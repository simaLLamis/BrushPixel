from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import uuid


# Create your models here.
class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    style = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    website = models.URLField(blank=True)
    social_instagram = models.CharField(max_length=100, blank=True)
    social_facebook = models.CharField(max_length=100, blank=True)
    social_twitter = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    @property
    def artwork_count(self):
        return self.artworks.count()

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    preferences = models.ManyToManyField('listings.ArtCategory', blank=True, related_name='interested_customers')
    profile_image = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    newsletter_subscribed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()}"

class Review(models.Model):
    artwork = models.ForeignKey("listings.Artwork", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified_purchase = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('artwork', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.artwork.title}"



class Commission(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_commissions')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='commissions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    requested_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    reference_images = models.ManyToManyField('CommissionReferenceImage', blank=True)
    
    def __str__(self):
        return f"Commission: {self.title} ({self.get_status_display()})"

class CommissionReferenceImage(models.Model):
    image = models.ImageField(upload_to='commission_references/')
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Reference Image {self.id}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey("listings.Artwork", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.artwork.title}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percent = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    single_use = models.BooleanField(default=False)
    
    def __str__(self):
        if self.discount_amount:
            return f"{self.code} (${self.discount_amount} off)"
        return f"{self.code} ({self.discount_percent}% off)"
    
    @property
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    artwork = models.ForeignKey("listings.Artwork", on_delete=models.CASCADE, related_name='bookmarks')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'artwork')
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.artwork.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order_update', 'Order Update'),
        ('artwork_update', 'Artwork Update'),
        ('commission_update', 'Commission Update'),
        ('new_message', 'New Message'),
        ('price_drop', 'Price Drop'),
        ('system', 'System Notification'),
        ('review', 'New Review'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    linked_url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    artwork = models.ForeignKey("listings.Artwork", on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.recipient.username}"

class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    exhibitions = models.BooleanField(default=False)
    artists = models.BooleanField(default=False)
    events = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification settings for {self.user.username}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total(self):
        return sum(item.artwork.price * item.quantity for item in self.items.all())
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey("listings.Artwork", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    saved_for_later = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('cart', 'artwork')
    
    def __str__(self):
        return f"{self.quantity} x {self.artwork.title} in {self.cart}"
    
    
    
    
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """Create a CustomerProfile for each new User"""
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """Save the CustomerProfile when the User is saved"""
    instance.customer_profile.save()
    
    
    
@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    """Create NotificationSettings for each new User"""
    if created:
        NotificationSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_notification_settings(sender, instance, **kwargs):
    """Save the NotificationSettings when the User is saved"""
    if hasattr(instance, 'notification_settings'):
        instance.notification_settings.save()
        
        