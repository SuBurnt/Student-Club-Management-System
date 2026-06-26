from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1
    readonly_fields = ('registered_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'club',
        'date_time',
        'location',
        'max_participants',
        'registered_count')
    list_filter = ('club', 'date_time')
    search_fields = ('title', 'description')
    inlines = [EventRegistrationInline]

    def registered_count(self, obj):
        return obj.registrations.filter(status='confirmed').count()
    registered_count.short_description = 'Зарегистрировано'

    actions = ['cancel_all_registrations']

    def cancel_all_registrations(self, request, queryset):
        for event in queryset:
            event.registrations.update(status='cancelled')
        self.message_user(
            request, f'Регистрации отменены для {
                queryset.count()} мероприятий')
    cancel_all_registrations.short_description = 'Отменить все регистрации'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'registered_at')
    list_filter = ('status', 'event')
