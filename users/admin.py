from django.contrib import admin
from users.models import User, Profile

class ProfileInline(admin.TabularInline):
    model = Profile
    
# Register your models here.
@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    inlines = [ProfileInline]
