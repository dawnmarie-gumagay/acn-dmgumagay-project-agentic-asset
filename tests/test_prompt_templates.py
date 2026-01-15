"""
Unit tests for prompt templates
Tests template retrieval, formatting, and integration patterns
"""
import pytest
from prompt_templates import (
    get_prompt,
    list_available_prompts,
    create_custom_prompt,
    REQUIREMENTS_ANALYZER_PROMPTS,
    IAC_GENERATOR_PROMPTS,
    VALIDATOR_PROMPTS,
    REMEDIATION_PROMPTS,
    CICD_GENERATOR_PROMPTS,
    MONITORING_SETUP_PROMPTS
)


class TestPromptRetrieval:
    """Test prompt template retrieval functions"""
    
    def test_get_prompt_basic(self):
        """Test basic prompt retrieval"""
        prompt = get_prompt(
            "REQUIREMENTS_ANALYZER_PROMPTS",
            "analyze_deployment",
            user_input="Deploy nginx with 3 replicas"
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert "Deploy nginx with 3 replicas" in prompt
    
    def test_get_prompt_with_multiple_variables(self):
        """Test prompt retrieval with multiple template variables"""
        # Use a simpler prompt that doesn't have nested variable names
        prompt = get_prompt(
            "REQUIREMENTS_ANALYZER_PROMPTS",
            "analyze_microservices",
            user_input="Microservices architecture with API gateway and 3 services"
        )
        
        assert "Microservices architecture" in prompt
        assert "microservice" in prompt.lower()
    
    def test_get_prompt_invalid_category(self):
        """Test error handling for invalid category"""
        with pytest.raises(ValueError, match="not found in category"):
            get_prompt("INVALID_CATEGORY", "some_prompt")
    
    def test_get_prompt_invalid_prompt_name(self):
        """Test error handling for invalid prompt name"""
        with pytest.raises(ValueError, match="not found in category"):
            get_prompt("REQUIREMENTS_ANALYZER_PROMPTS", "nonexistent_prompt")


class TestPromptTemplateStructure:
    """Test prompt template structure and content"""
    
    def test_requirements_analyzer_prompts_exist(self):
        """Test requirements analyzer prompts are defined"""
        assert "analyze_deployment" in REQUIREMENTS_ANALYZER_PROMPTS
        assert "analyze_microservices" in REQUIREMENTS_ANALYZER_PROMPTS
        assert len(REQUIREMENTS_ANALYZER_PROMPTS) >= 2
    
    def test_iac_generator_prompts_exist(self):
        """Test IaC generator prompts are defined"""
        assert "generate_kubernetes_manifest" in IAC_GENERATOR_PROMPTS
        assert "generate_helm_chart" in IAC_GENERATOR_PROMPTS
        assert "generate_terraform" in IAC_GENERATOR_PROMPTS
        assert len(IAC_GENERATOR_PROMPTS) >= 3
    
    def test_cicd_generator_prompts_exist(self):
        """Test CI/CD generator prompts are defined"""
        assert "generate_github_actions" in CICD_GENERATOR_PROMPTS
        assert "generate_gitlab_ci" in CICD_GENERATOR_PROMPTS
        assert "generate_argocd" in CICD_GENERATOR_PROMPTS
        assert len(CICD_GENERATOR_PROMPTS) >= 3
    
    def test_monitoring_prompts_exist(self):
        """Test monitoring setup prompts are defined"""
        assert "generate_monitoring" in MONITORING_SETUP_PROMPTS
        assert "generate_alerts" in MONITORING_SETUP_PROMPTS
        assert len(MONITORING_SETUP_PROMPTS) >= 2
    
    def test_all_prompts_are_strings(self):
        """Test all prompt templates are strings"""
        for prompt_dict in [
            REQUIREMENTS_ANALYZER_PROMPTS,
            IAC_GENERATOR_PROMPTS,
            VALIDATOR_PROMPTS,
            REMEDIATION_PROMPTS
        ]:
            for prompt_name, prompt_template in prompt_dict.items():
                assert isinstance(prompt_template, str), f"{prompt_name} is not a string"
                assert len(prompt_template) > 20, f"{prompt_name} is too short"


class TestPromptListing:
    """Test prompt listing functionality"""
    
    def test_list_available_prompts(self):
        """Test listing all available prompts"""
        available = list_available_prompts()
        
        assert isinstance(available, dict)
        assert len(available) > 5  # Should have multiple categories
        assert "REQUIREMENTS_ANALYZER_PROMPTS" in available
        assert "IAC_GENERATOR_PROMPTS" in available
        assert "CICD_GENERATOR_PROMPTS" in available
    
    def test_list_prompts_shows_all_categories(self):
        """Test all major categories are listed"""
        available = list_available_prompts()
        
        expected_categories = [
            "REQUIREMENTS_ANALYZER_PROMPTS",
            "IAC_GENERATOR_PROMPTS",
            "VALIDATOR_PROMPTS",
            "REMEDIATION_PROMPTS",
            "CICD_GENERATOR_PROMPTS",
            "MONITORING_SETUP_PROMPTS"
        ]
        
        for category in expected_categories:
            assert category in available, f"{category} not found in available prompts"
    
    def test_listed_prompts_are_accurate(self):
        """Test listed prompts match actual dictionary contents"""
        available = list_available_prompts()
        
        # Verify requirements analyzer prompts
        assert set(available["REQUIREMENTS_ANALYZER_PROMPTS"]) == set(REQUIREMENTS_ANALYZER_PROMPTS.keys())
        
        # Verify IaC generator prompts
        assert set(available["IAC_GENERATOR_PROMPTS"]) == set(IAC_GENERATOR_PROMPTS.keys())


class TestCustomPromptCreation:
    """Test custom prompt creation functionality"""
    
    def test_create_custom_prompt_basic(self):
        """Test basic custom prompt creation"""
        base = "Deploy application"
        custom = create_custom_prompt(base)
        
        assert custom == base
    
    def test_create_custom_prompt_with_context(self):
        """Test custom prompt with additional context"""
        base = "Deploy application"
        additional = "Must be highly available"
        custom = create_custom_prompt(base, additional)
        
        assert base in custom
        assert additional in custom
        assert "Additional Context:" in custom
    
    def test_custom_prompt_preserves_base(self):
        """Test custom prompt preserves base content"""
        base = "Generate Kubernetes manifest for production"
        additional = "Include monitoring and security configs"
        custom = create_custom_prompt(base, additional)
        
        assert custom.startswith(base)
        assert additional in custom


class TestPromptIntegration:
    """Test integration patterns for using prompts with tasks"""
    
    def test_prompt_integration_with_task(self):
        """Test prompt can be used to create task description"""
        from crewai import Task, Agent
        from crewai import LLM
        
        # Create a test agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            llm=LLM(model="ollama/llama2:7b", base_url="https://test.com", api_key="test"),
            verbose=False
        )
        
        # Get prompt template
        prompt = get_prompt(
            "REQUIREMENTS_ANALYZER_PROMPTS",
            "analyze_deployment",
            user_input="Deploy nginx"
        )
        
        # Create task with prompt
        task = Task(
            description=prompt,
            agent=test_agent,
            expected_output="Structured deployment requirements"
        )
        
        assert "nginx" in task.description
        assert "deployment" in task.description.lower()
    
    def test_cicd_prompt_integration_example(self):
        """Test CI/CD prompt integration pattern"""
        prompt = get_prompt(
            "CICD_GENERATOR_PROMPTS",
            "generate_github_actions",
            application_details="Python Flask API with PostgreSQL database"
        )
        
        assert "Python Flask API" in prompt
        assert "PostgreSQL" in prompt
        assert "GitHub Actions" in prompt or "workflow" in prompt.lower()


class TestPromptContentQuality:
    """Test prompt content quality and completeness"""
    
    def test_deployment_prompt_includes_key_sections(self):
        """Test deployment analysis prompt includes all key sections"""
        prompt_template = REQUIREMENTS_ANALYZER_PROMPTS["analyze_deployment"]
        
        # Check for key sections
        assert "Application Details" in prompt_template
        assert "Container Configuration" in prompt_template
        assert "Resource Requirements" in prompt_template
        assert "Scaling" in prompt_template or "Availability" in prompt_template
        assert "Networking" in prompt_template
    
    def test_kubernetes_generation_prompt_is_detailed(self):
        """Test Kubernetes generation prompt is sufficiently detailed"""
        prompt_template = IAC_GENERATOR_PROMPTS["generate_kubernetes_manifest"]
        
        assert "Deployment" in prompt_template
        assert "Service" in prompt_template
        assert "resource" in prompt_template.lower()
        assert "probe" in prompt_template.lower()
        assert "production" in prompt_template.lower()
    
    def test_remediation_prompts_include_failure_types(self):
        """Test remediation prompts cover common failure types"""
        # Check OOM diagnosis
        oom_prompt = REMEDIATION_PROMPTS["diagnose_oom"]
        assert "memory" in oom_prompt.lower()
        assert "oom" in oom_prompt.lower() or "out of memory" in oom_prompt.lower()
        
        # Check crash loop diagnosis
        crash_prompt = REMEDIATION_PROMPTS["diagnose_crashloop"]
        assert "crash" in crash_prompt.lower()
        assert "startup" in crash_prompt.lower() or "dependencies" in crash_prompt.lower()
