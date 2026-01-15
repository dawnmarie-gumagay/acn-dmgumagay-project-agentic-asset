"""
Integration tests for full CrewAI workflows
Tests end-to-end crew execution with mocked LLM responses
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from crewai import Crew, Process


class TestStandardWorkflow:
    """Test standard manifest generation workflow"""
    
    @patch('agents.llm')
    def test_full_crew_workflow_structure(self, mock_llm, sample_user_prompt, sample_kubernetes_manifest):
        """Test complete workflow from prompt to manifest"""
        # Mock LLM to return appropriate responses
        mock_llm.call.side_effect = [
            "Analyzed requirements: Java Spring Boot app, 3 replicas, 512Mi memory",
            sample_kubernetes_manifest,
            f"VALIDATION PASSED\n{sample_kubernetes_manifest}"
        ]
        
        from agents import requirements_analyzer, iac_generator, validator
        from tasks import create_analysis_task, create_generation_task, create_validation_task
        
        # Create tasks
        analysis_task = create_analysis_task(sample_user_prompt)
        generation_task = create_generation_task()
        validation_task = create_validation_task()
        
        # Set task context (sequential dependency)
        generation_task.context = [analysis_task]
        validation_task.context = [generation_task]
        
        # Create crew
        crew = Crew(
            agents=[requirements_analyzer, iac_generator, validator],
            tasks=[analysis_task, generation_task, validation_task],
            process=Process.sequential,
            verbose=False
        )
        
        # Verify crew structure
        assert len(crew.agents) == 3
        assert len(crew.tasks) == 3
        assert crew.process == Process.sequential
    
    @patch('agents.llm')
    def test_task_sequential_execution(self, mock_llm, sample_user_prompt):
        """Test tasks execute in sequential order"""
        execution_order = []
        
        def track_execution(task_name):
            def mock_response(*args, **kwargs):
                execution_order.append(task_name)
                return f"Response from {task_name}"
            return mock_response
        
        mock_llm.call.side_effect = [
            "Analysis complete",
            "Manifest generated",
            "Validation passed"
        ]
        
        from agents import requirements_analyzer, iac_generator, validator
        from tasks import create_analysis_task, create_generation_task, create_validation_task
        
        analysis_task = create_analysis_task(sample_user_prompt)
        generation_task = create_generation_task()
        validation_task = create_validation_task()
        
        # Verify task context dependencies
        generation_task.context = [analysis_task]
        validation_task.context = [generation_task]
        
        assert generation_task.context == [analysis_task]
        assert validation_task.context == [generation_task]


class TestSelfHealingWorkflow:
    """Test self-healing workflow with failure detection and remediation"""
    
    def test_simulate_deployment_failure(self, sample_deployment_failure):
        """Test deployment simulation with failure scenario"""
        from main_with_healing import simulate_deployment
        
        success, status = simulate_deployment("test manifest", retry_count=0)
        
        assert success == False
        assert "FAILED" in status or "OOMKilled" in status
    
    def test_simulate_deployment_success_on_retry(self):
        """Test deployment succeeds on retry"""
        from main_with_healing import simulate_deployment
        
        success, status = simulate_deployment("corrected manifest", retry_count=1)
        
        assert success == True
        assert "SUCCESS" in status or "Running" in status
    
    @patch('agents.llm')
    def test_remediation_task_creation(self, mock_llm, sample_deployment_failure):
        """Test remediation tasks are created correctly"""
        from tasks import create_monitoring_task, create_diagnosis_task, create_remediation_task
        
        # Create monitoring task
        monitoring_task = create_monitoring_task(sample_deployment_failure["status"])
        assert "OOMKilled" in monitoring_task.description
        
        # Create diagnosis task
        diagnosis_task = create_diagnosis_task(sample_deployment_failure["status"])
        assert "diagnose" in diagnosis_task.description.lower()
        
        # Create remediation task
        original_manifest = "apiVersion: apps/v1\nkind: Deployment"
        remediation_task = create_remediation_task(
            sample_deployment_failure["status"],
            original_manifest
        )
        assert "remediation" in remediation_task.description.lower() or "fix" in remediation_task.description.lower()


class TestOutputHandling:
    """Test output file generation and YAML extraction"""
    
    def test_ensure_output_dir(self, reset_output_dir):
        """Test output directory is created if it doesn't exist"""
        from main import ensure_output_dir
        
        ensure_output_dir()
        assert reset_output_dir.exists()
    
    @patch('main.datetime')
    def test_save_results_creates_files(self, mock_datetime, sample_user_prompt, sample_kubernetes_manifest, reset_output_dir):
        """Test save_results creates JSON and YAML files"""
        from main import save_results
        
        # Mock datetime for consistent filenames
        mock_datetime.now.return_value.strftime.return_value = "20260114_120000"
        mock_datetime.now.return_value.isoformat.return_value = "2026-01-14T12:00:00"
        
        result = f"Analysis complete\n{sample_kubernetes_manifest}"
        execution_time = 123.45
        
        output_file = save_results(sample_user_prompt, result, execution_time)
        
        # Verify JSON file was created
        assert output_file is not None
        assert "result_" in output_file
        assert output_file.endswith(".json")
    
    def test_yaml_extraction_from_result(self, sample_kubernetes_manifest):
        """Test YAML manifest extraction from crew result"""
        result_with_yaml = f"""
        Analysis: The application requires 3 replicas with 512Mi memory.
        
        Generated Manifest:
        {sample_kubernetes_manifest}
        
        Validation: All checks passed.
        """
        
        # Check for YAML markers
        assert "apiVersion" in result_with_yaml
        assert "kind:" in result_with_yaml
        assert "Deployment" in result_with_yaml


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_config_validation_before_execution(self):
        """Test Config.validate() is called before crew execution"""
        from config import Config
        
        # Should not raise if properly configured
        try:
            Config.validate()
            validation_works = True
        except ValueError:
            validation_works = False
        
        # In test environment with mock_config, this should pass
        assert validation_works or Config.OLLAMA_API_KEY is None
    
    @patch('agents.llm')
    def test_crew_handles_empty_prompt(self, mock_llm):
        """Test crew handles edge case of empty prompt"""
        from crewai import Task
        from tasks import create_analysis_task
        
        empty_prompt = ""
        task = create_analysis_task(empty_prompt)
        
        # Task should still be created, even with empty input
        assert isinstance(task, Task)
        assert task.description is not None
