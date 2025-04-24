from django.db import models

from accounts.models import ArtistProfile
# Create your models here.
class ArtCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Art Categories"
    
    def __str__(self):
        return self.name

class Artwork(models.Model):
    MEDIUM_CHOICES = [
        ('oil', 'Oil on Canvas'),
        ('acrylic', 'Acrylic'),
        ('watercolor', 'Watercolor'),
        ('digital', 'Digital Art'),
        ('photography', 'Photography'),
        ('mixed', 'Mixed Media'),
        ('sculpture', 'Sculpture'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('on_display', 'On Display'),
    ]
    
    FRAMING_CHOICES = [
        ('unframed', 'Unframed'),
        ('framed', 'Framed'),
        ('gallery_wrapped', 'Gallery Wrapped'),
        ('matted', 'Matted'),
    ]
    
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='artworks')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    medium = models.CharField(max_length=20, choices=MEDIUM_CHOICES)
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in inches/cm")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in inches/cm")
    depth = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Depth in inches/cm (if applicable)")
    year_created = models.IntegerField()
    categories = models.ManyToManyField(ArtCategory, related_name='artworks')
    style = models.CharField(max_length=100, blank=True)
    framing = models.CharField(max_length=20, choices=FRAMING_CHOICES, default='unframed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_original = models.BooleanField(default=True)
    has_certificate = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=255)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} by {self.artist.user.get_full_name()}"
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def dimensions(self):
        if self.depth and self.depth > 0:
            return f"{self.width}\" × {self.height}\" × {self.depth}\""
        return f"{self.width}\" × {self.height}\""

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artwork_images/')
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.artwork.title}"
