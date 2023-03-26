from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Subscription, User


class UserAdmin(ModelAdmin):
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
