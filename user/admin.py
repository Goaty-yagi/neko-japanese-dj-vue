from django.contrib import admin
from .models import User,IPData
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User as AuthUser
# Register your models here.
# class UserInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'user'

# class UserAdmin(UserAdmin):
#     inlines = (UserInline,)

# admin.site.unregister(AuthUser)
admin.site.register(User)
admin.site.register(IPData)