from django.contrib import admin
from market.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административная панель для модели Product"""
    list_display = ('title', 'price')
    fieldsets = (
        (None, {'fields': ('title',)}),
        ('Цена', {'fields': ('cost_price', 'price')}),
        ('Описание', {'fields': ('description', 'image')}),
        ('Продавец', {'fields': ('owner',)}),
        ('Публичность', {'fields': ('is_published',)})
    )
