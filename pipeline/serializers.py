from rest_framework import serializers
from .models import (
    Task, Vendor, Timeline, Subtask, 
    CapabilityMapping, FinalAnalysis, ValidationLog
)

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['id', 'phase', 'year', 'aps_score', 'capability_description', 'source']

class VendorSerializer(serializers.ModelSerializer):
    timeline = TimelineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'vendor_name', 'product_name', 'status', 
                  'evidence_url', 'source', 'aps_2024', 'aps_2025', 'aps_2026', 
                  'is_verified', 'created_at', 'timeline']

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'subtask_name', 'description', 'time_percent', 'importance', 
                  'ai_applicable', 'onet_weight']

class CapabilityMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.vendor_name', read_only=True)
    subtask_name = serializers.CharField(source='subtask.subtask_name', read_only=True)
    
    class Meta:
        model = CapabilityMapping
        fields = ['id', 'vendor_name', 'subtask_name', 'can_handle', 
                  'aps_2024', 'aps_2025', 'aps_2026', 'improvement_rate']

class FinalAnalysisSerializer(serializers.ModelSerializer):
    best_vendor_name = serializers.CharField(source='best_vendor.vendor_name', read_only=True)
    
    class Meta:
        model = FinalAnalysis
        fields = ['id', 'best_vendor_name', 'automation_2024', 'automation_2025', 
                  'automation_2026', 'hrf_scores', 'rpi_score', 'recommendations']

class TaskSerializer(serializers.ModelSerializer):
    vendors = VendorSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    final_analysis = FinalAnalysisSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'task_description', 'status', 'created_at', 
                  'updated_at', 'error_message', 'vendors', 'subtasks', 'final_analysis']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user_id', 'task_description']