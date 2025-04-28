from django.contrib import admin
from .models import Artwork, ArtworkImage

class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1
    fields = ('image', 'is_primary', 'order')

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'price', 'medium', 'year_created', 'status', 'featured', 'is_new')
    list_filter = ('status', 'medium', 'featured', 'is_new', 'is_original', 'has_certificate', 'year_created')
    search_fields = ('title', 'description', 'artist__user__username', 'style')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArtworkImageInline]
    readonly_fields = ('views', 'date_added')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'artist', 'description', 'price', 'medium')
        }),
        ('Artwork Details', {
            'fields': ('width', 'height', 'depth', 'year_created', 'style', 'framing')
        }),
        ('Status', {
            'fields': ('status', 'is_original', 'has_certificate', 'featured', 'is_new')
        }),
        ('Analytics', {
            'fields': ('views', 'date_added')
        }),
    )

@admin.register(ArtworkImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'image', 'is_primary', 'order')
    list_filter = ('is_primary',)
    search_fields = ('artwork__title', 'artwork__description')
    fields = ('artwork', 'image', 'is_primary', 'order')