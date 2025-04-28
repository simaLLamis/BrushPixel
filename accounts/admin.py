from django.contrib import admin

# Register your models here.
from .models import (
    ArtistProfile, CustomerProfile, Review, Commission, 
    CommissionReferenceImage, Order, OrderItem, Coupon, 
    Bookmark, Notification, NotificationSettings, Cart, CartItem
)

# Artist Profile Admin
@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'featured', 'style', 'joined_date')
    list_filter = ('featured', 'joined_date')
    search_fields = ('user__username', 'user__email', 'bio', 'location')

# Customer Profile Admin
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'country', 'newsletter_subscribed')
    list_filter = ('newsletter_subscribed', 'country', 'state')
    search_fields = ('user__username', 'user__email', 'phone', 'city')

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'user', 'rating', 'title', 'created_at', 'verified_purchase')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'artwork__title')

# Commission Admin
@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'artist', 'status', 'price', 'requested_date', 'completion_date')
    list_filter = ('status', 'requested_date', 'completion_date')
    search_fields = ('title', 'description', 'client__username', 'artist__user__username')

# Commission Reference Image Admin
@admin.register(CommissionReferenceImage)
class CommissionReferenceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description',)

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'shipping_address_line1', 'tracking_number')
    readonly_fields = ('order_number',)

# Order Item Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'artwork', 'price', 'quantity')
    search_fields = ('order__order_number', 'artwork__title')

# Coupon Admin
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'discount_percent', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('is_active', 'valid_from', 'valid_to', 'single_use')
    search_fields = ('code', 'description')

# Bookmark Admin
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'artwork__title')

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'type', 'title', 'created_at', 'read')
    list_filter = ('type', 'read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')

# Notification Settings Admin
@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'exhibitions', 'artists', 'events')
    list_filter = ('exhibitions', 'artists', 'events')
    search_fields = ('user__username',)

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'item_count', 'total')
    search_fields = ('user__username',)

# Cart Item Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'artwork', 'quantity', 'date_added', 'saved_for_later')
    list_filter = ('saved_for_later', 'date_added')
    search_fields = ('cart__user__username', 'artwork__title')