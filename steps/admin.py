from django.contrib import admin

from steps.models import Step


# Register your models here.
@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('target_goal', 'title', 'completed')
    list_filter = ('completed',)
    search_fields = ('title',)
    ordering = ('-completed_at',)
    date_hierarchy = 'completed_at'
    list_editable = ('completed',)
    readonly_fields = ('completed_at',)