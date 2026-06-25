from django.contrib import admin
from .models import DiscussionTopic, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(DiscussionTopic)
class DiscussionTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'created_by', 'created_at', 'comments_count')
    list_filter = ('club', 'created_at')
    search_fields = ('title', 'content')
    inlines = [CommentInline]
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Комментариев'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'created_at')
    list_filter = ('topic__club', 'created_at')