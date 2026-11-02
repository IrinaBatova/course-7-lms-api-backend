from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from users.models import User


# Создаем простой класс настроек без привязки к стандартному username
# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     # Указываем, какие поля показывать в таблице админки
#     list_display = ('id', 'email', 'is_staff', 'is_superuser', 'is_active')
#
#     # Поиск по email:
#     search_fields = ('email',)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('id', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # ВЫВОДИМ ДВА ПОЛЯ ДЛЯ ПАРОЛЯ, ЧТОБЫ ФОРМА СТАЛА ВАЛИДНОЙ
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password',
                       'password_confirmation' if hasattr(UserCreationForm, 'password_confirmation') else 'password'),
        }),
    )