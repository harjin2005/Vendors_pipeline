 
from django.db import models
from django.utils import timezone
import json

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('phase1_running', 'Phase 1 Running'),
        ('phase1_done', 'Phase 1 Done'),
        ('phase2_running', 'Phase 2 Running'),
        ('phase2_done', 'Phase 2 Done'),
        ('phase3_running', 'Phase 3 Running'),
        ('phase3_done', 'Phase 3 Done'),
        ('phase4_running', 'Phase 4 Running'),
        ('phase4_done', 'Phase 4 Done'),
        ('phase5_running', 'Phase 5 Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    
    user_id = models.CharField(max_length=100, db_index=True)
    task_description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Task {self.id}: {self.task_description[:50]}"

class Vendor(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='vendors')
    vendor_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    evidence_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=255, default='discovery')
    status = models.CharField(max_length=50, default='discovered')
    aps_2024 = models.FloatField(default=0.7, null=True)
    aps_2025 = models.FloatField(default=0.8, null=True)
    aps_2026 = models.FloatField(default=0.9, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vendors'
    
    def __str__(self):
        return self.vendor_name

class Timeline(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='timeline')
    phase = models.CharField(max_length=50)
    year = models.IntegerField()
    aps_score = models.FloatField()
    capability_description = models.TextField()
    source = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'timeline'
        unique_together = ['vendor', 'phase', 'year']
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.phase} {self.year}"

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    subtask_name = models.CharField(max_length=200)
    description = models.TextField()
    time_percent = models.FloatField()
    importance = models.FloatField()
    ai_applicable = models.CharField(max_length=20)
    onet_weight = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subtasks'
    
    def __str__(self):
        return f"{self.task_id}: {self.subtask_name}"

class CapabilityMapping(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='capability_mappings')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    can_handle = models.CharField(max_length=20)
    aps_2024 = models.FloatField(null=True, blank=True)
    aps_2025 = models.FloatField(null=True, blank=True)
    aps_2026 = models.FloatField(null=True, blank=True)
    improvement_rate = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'capability_mapping'
        unique_together = ['vendor', 'subtask']
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.subtask.subtask_name}"

class FinalAnalysis(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='final_analysis')
    best_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    automation_2024 = models.FloatField()
    automation_2025 = models.FloatField()
    automation_2026 = models.FloatField()
    hrf_scores = models.JSONField()
    rpi_score = models.FloatField()
    recommendations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'final_analysis'
    
    def __str__(self):
        return f"Analysis for Task {self.task_id}"

class ValidationLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='validation_logs')
    phase = models.CharField(max_length=50)
    validation_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'validation_logs'
    
    def __str__(self):
        return f"{self.phase} - {self.status}"