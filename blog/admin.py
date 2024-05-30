from django.contrib import admin
from .models import Post, Paragraph

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]

admin.site.register(Post, PostAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

