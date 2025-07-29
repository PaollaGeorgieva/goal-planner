from django.contrib import admin

from goals.models import Category, TargetGoal, HabitGoal, HabitCheck


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('is_system', 'created_by__email')
    search_fields = ('name',)
    ordering = ('-is_system', 'name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(TargetGoal)
class TargetGoalAdmin(admin.ModelAdmin):
    list_display = ('title',  'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed', 'end_date', 'category')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-end_date',)
    date_hierarchy = 'end_date'
    list_editable = ('is_completed',)
    readonly_fields = ('completed_at', 'progress_percent')


@admin.register(HabitGoal)
class HabitGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_completed')
    list_filter = ('period_unit', 'is_completed')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_completed',)
    readonly_fields = ('completed_at', 'progress_percent')



@admin.register(HabitCheck)
class HabitCheckAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date')
    list_filter = ('date', 'habit__title')
    search_fields = ('habit__title',)
    ordering = ('-date',)
    date_hierarchy = 'date'
