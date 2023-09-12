from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административная панель для модели User"""
    list_display = ('email', 'phone')
    fieldsets = (
        (None, {'fields': ('email', )}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'role', 'phone')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')})
    )
