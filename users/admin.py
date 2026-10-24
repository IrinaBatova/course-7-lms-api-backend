from django.contrib import admin
from  django.contrib.auth.admin import UserAdmin
from users.models import User


# Создаем простой класс настроек без привязки к стандартному username
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Указываем, какие поля показывать в таблице админки
    list_display = ('id', 'email', 'is_staff', 'is_superuser', 'is_active')

    # Поиск по email:
    search_fields = ('email',)
