from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Subscription, User


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')


class SubscriptionAdmin(ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
