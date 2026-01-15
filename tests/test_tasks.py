"""
Unit tests for CrewAI tasks
Tests task creation, descriptions, and expected outputs
"""
import pytest
from crewai import Task


class TestTaskCreation:
    """Test task factory functions"""
    
    def test_create_analysis_task(self, sample_user_prompt):
        """Test analysis task creation with user prompt"""
        from tasks import create_analysis_task
        
        task = create_analysis_task(sample_user_prompt)
        
        assert isinstance(task, Task)
        assert sample_user_prompt in task.description
        assert "extract" in task.description.lower()
        assert task.agent is not None
        assert task.expected_output is not None
    
    def test_create_generation_task(self):
        """Test generation task creation"""
        from tasks import create_generation_task
        
        task = create_generation_task()
        
        assert isinstance(task, Task)
        assert "yaml" in task.description.lower()
        assert "kubernetes" in task.description.lower()
        assert "deployment" in task.description.lower()
        assert "manifest" in task.expected_output.lower()
    
    def test_create_validation_task(self):
        """Test validation task creation"""
        from tasks import create_validation_task
        
        task = create_validation_task()
        
        assert isinstance(task, Task)
        assert "validate" in task.description.lower()
        assert "yaml" in task.description.lower()
        assert "validation" in task.expected_output.lower()
    
    def test_create_monitoring_task(self, sample_deployment_failure):
        """Test monitoring task creation with deployment status"""
        from tasks import create_monitoring_task
        
        task = create_monitoring_task(sample_deployment_failure["status"])
        
        assert isinstance(task, Task)
        assert "oomkilled" in task.description.lower()
        assert "failure" in task.description.lower()
    
    def test_create_diagnosis_task(self):
        """Test diagnosis task creation"""
        from tasks import create_diagnosis_task
        
        failure_info = "OOMKilled: Memory limit exceeded"
        task = create_diagnosis_task(failure_info)
        
        assert isinstance(task, Task)
        assert failure_info in task.description
        assert "diagnose" in task.description.lower()
        assert "root cause" in task.description.lower()
    
    def test_create_remediation_task(self, sample_kubernetes_manifest):
        """Test remediation task creation"""
        from tasks import create_remediation_task
        
        diagnosis = "Memory limit too low"
        task = create_remediation_task(diagnosis, sample_kubernetes_manifest)
        
        assert isinstance(task, Task)
        assert diagnosis in task.description
        assert sample_kubernetes_manifest in task.description


class TestTaskDescriptions:
    """Test task description quality and completeness"""
    
    def test_analysis_task_includes_key_points(self, sample_user_prompt):
        """Test analysis task description includes all required extraction points"""
        from tasks import create_analysis_task
        
        task = create_analysis_task(sample_user_prompt)
        description = task.description.lower()
        
        # Check for key extraction points
        assert "application name" in description
        assert "container image" in description or "image" in description
        assert "port" in description
        assert "replicas" in description
        assert "resource" in description or "cpu" in description or "memory" in description
    
    def test_generation_task_includes_k8s_structure(self):
        """Test generation task describes complete K8s manifest structure"""
        from tasks import create_generation_task
        
        task = create_generation_task()
        description = task.description.lower()
        
        assert "apiversion" in description
        assert "metadata" in description
        assert "spec" in description
        assert "replicas" in description
        assert "selector" in description
        assert "resources" in description
        assert "probe" in description
    
    def test_validation_task_includes_checks(self):
        """Test validation task describes all validation checks"""
        from tasks import create_validation_task
        
        task = create_validation_task()
        description = task.description.lower()
        
        assert "yaml syntax" in description
        assert "required" in description and "fields" in description
        assert "resource" in description and "limits" in description
        assert "labels" in description
        assert "best practices" in description


class TestTaskExpectedOutputs:
    """Test expected output specifications"""
    
    def test_tasks_have_clear_expected_outputs(self):
        """Test all tasks have clear expected output specifications"""
        from tasks import (
            create_analysis_task,
            create_generation_task,
            create_validation_task
        )
        
        analysis_task = create_analysis_task("Deploy nginx")
        generation_task = create_generation_task()
        validation_task = create_validation_task()
        
        assert len(analysis_task.expected_output) > 20
        assert len(generation_task.expected_output) > 20
        assert len(validation_task.expected_output) > 20
        
        assert "summary" in analysis_task.expected_output.lower() or "structured" in analysis_task.expected_output.lower()
        assert "yaml" in generation_task.expected_output.lower() or "manifest" in generation_task.expected_output.lower()
        assert "validation" in validation_task.expected_output.lower()
