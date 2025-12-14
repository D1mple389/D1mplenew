from django.contrib import admin
from .models import ForumThread, Post

@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_locked')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
