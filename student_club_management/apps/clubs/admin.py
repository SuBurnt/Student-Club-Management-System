from django.contrib import admin
from .models import Club, ClubMember

class ClubMemberInline(admin.TabularInline):
    """Встроенное отображение участников клуба."""
    model = ClubMember
    extra = 1
    readonly_fields = ('joined_at',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Админка для клубов."""
    list_display = ('name', 'category', 'owner', 'created_at', 'members_count')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    inlines = [ClubMemberInline]
    readonly_fields = ('created_at',)
    
    def members_count(self, obj):
        return obj.clubmember_set.count()
    members_count.short_description = 'Участников'
    
    actions = ['delete_selected_clubs']
    
    def delete_selected_clubs(self, request, queryset):
        """Массовое удаление клубов."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Удалено клубов: {count}')
    delete_selected_clubs.short_description = 'Удалить выбранные клубы'


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'role', 'joined_at')
    list_filter = ('role', 'club')
