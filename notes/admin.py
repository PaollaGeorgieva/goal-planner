from django.contrib import admin

from notes.models import Note


# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display    = ('title', 'goal', 'created_at')
    list_filter     = ('content_type', 'created_at')
    search_fields   = ('title', 'content')
    ordering        = ('-created_at',)
    date_hierarchy  = 'created_at'
    readonly_fields = ('created_at',)
