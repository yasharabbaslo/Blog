from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Author, Newsletter, Message


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)   # Gives an advanced editor for body field
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')


@admin.register(Message)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created')
    search_fields = ('name', 'email', 'subject', 'body')


admin.site.register(Author)
admin.site.register(Newsletter)