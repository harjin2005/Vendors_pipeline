 
from django.contrib import admin
from .models import (
    Task, Vendor, Timeline, Subtask, 
    CapabilityMapping, FinalAnalysis, ValidationLog
)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_id', 'task_description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'product_name', 'status', 'is_verified', 'task')
    list_filter = ('is_verified', 'status')
    search_fields = ('vendor_name', 'product_name')

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'phase', 'year', 'aps_score')
    list_filter = ('phase', 'year')

@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('subtask_name', 'task', 'time_percent', 'importance')
    list_filter = ('task', 'ai_applicable')

@admin.register(CapabilityMapping)
class CapabilityMappingAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'subtask', 'can_handle', 'aps_2025')

@admin.register(FinalAnalysis)
class FinalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('task', 'best_vendor', 'automation_2025', 'rpi_score')

@admin.register(ValidationLog)
class ValidationLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'phase', 'status', 'created_at')
    list_filter = ('phase', 'status')