from django.contrib import admin
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin']
    readonly_fields = ['password']


admin.site.register(MyUser, MyUserAdmin)

