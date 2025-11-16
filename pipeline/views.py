from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
import asyncio
import json
import logging
import threading

from .models import Task, Vendor, Subtask, CapabilityMapping, FinalAnalysis, Timeline
from .serializers import TaskSerializer, VendorSerializer, SubtaskSerializer, TaskCreateSerializer
from .tasks.phase1 import run_phase1
from .tasks.phase2 import run_phase2
from .tasks.phase3 import run_phase3
from .tasks.phase4 import run_phase4
from .tasks.phase5 import run_phase5
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


def run_phase_in_thread(phase_func, task_id):
    """Run an async phase function in a new event loop in a thread"""
    def _run():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(phase_func(task_id))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Phase execution error: {e}", exc_info=True)
            raise
    
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=300)  # Wait up to 5 minutes
    return True

class TaskViewSet(viewsets.ModelViewSet):
    """Task API ViewSet - Create, list, and manage tasks"""
    queryset = Task.objects.prefetch_related('vendors', 'subtasks').all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]  # ← ADD THIS LINE
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new task"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        task = serializer.save(status='pending')
        
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def phase1(self, request, pk=None):
        """Run Phase 1: Vendor Discovery"""
        task = self.get_object()
        try:
            run_phase_in_thread(run_phase1, task.id)
            
            task.refresh_from_db()
            return Response(
                {'status': 'success', 'data': TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Phase 1 error: {e}")
            task.status = 'error'
            task.error_message = str(e)
            task.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def phase2(self, request, pk=None):
        """Run Phase 2: Timeline Analysis"""
        task = self.get_object()
        try:
            run_phase_in_thread(run_phase2, task.id)
            
            task.refresh_from_db()
            return Response(
                {'status': 'success', 'data': TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Phase 2 error: {e}")
            task.status = 'error'
            task.error_message = str(e)
            task.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def phase3(self, request, pk=None):
        """Run Phase 3: Subtask Decomposition"""
        task = self.get_object()
        try:
            run_phase_in_thread(run_phase3, task.id)
            
            task.refresh_from_db()
            return Response(
                {'status': 'success', 'data': TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Phase 3 error: {e}")
            task.status = 'error'
            task.error_message = str(e)
            task.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def phase4(self, request, pk=None):
        """Run Phase 4: Capability Mapping"""
        task = self.get_object()
        try:
            run_phase_in_thread(run_phase4, task.id)
            
            task.refresh_from_db()
            return Response(
                {'status': 'success', 'data': TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Phase 4 error: {e}")
            task.status = 'error'
            task.error_message = str(e)
            task.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def phase5(self, request, pk=None):
        """Run Phase 5: Final Calculation"""
        task = self.get_object()
        try:
            run_phase_in_thread(run_phase5, task.id)
            
            task.refresh_from_db()
            return Response(
                {'status': 'success', 'data': TaskSerializer(task).data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Phase 5 error: {e}")
            task.status = 'error'
            task.error_message = str(e)
            task.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Get final report for completed task"""
        task = self.get_object()
        
        try:
            analysis = FinalAnalysis.objects.get(task_id=task.id)
            return Response({
                'task_id': task.id,
                'task_description': task.task_description,
                'status': task.status,
                'automation_2024': analysis.automation_2024,
                'automation_2025': analysis.automation_2025,
                'automation_2026': analysis.automation_2026,
                'hrf_scores': analysis.hrf_scores,
                'rpi_score': analysis.rpi_score,
                'recommendations': analysis.recommendations,
                'best_vendor': analysis.best_vendor.vendor_name if analysis.best_vendor else None,
            })
        except FinalAnalysis.DoesNotExist:
            return Response(
                {'error': 'Analysis not completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    """Vendor API ViewSet - List and retrieve vendors"""
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if task_id:
            return Vendor.objects.filter(task_id=task_id)
        return Vendor.objects.all()

class SubtaskViewSet(viewsets.ReadOnlyModelViewSet):
    """Subtask API ViewSet - List and retrieve subtasks"""
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if task_id:
            return Subtask.objects.filter(task_id=task_id)
        return Subtask.objects.all()