"""
Unit tests for CrewAI agents
Tests agent initialization, configuration, and basic behavior
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from crewai import Agent
from crewai import LLM


class TestAgentInitialization:
    """Test agent creation and configuration"""
    
    def test_requirements_analyzer_initialization(self, mock_config):
        """Test requirements analyzer agent is properly initialized"""
        from agents import requirements_analyzer
        
        assert requirements_analyzer.role == 'DevOps Requirements Analyst'
        assert 'analyze user requirements' in requirements_analyzer.goal.lower()
        assert requirements_analyzer.allow_delegation == False
        assert requirements_analyzer.llm is not None
    
    def test_iac_generator_initialization(self, mock_config):
        """Test IaC generator agent is properly initialized"""
        from agents import iac_generator
        
        assert iac_generator.role == 'Infrastructure as Code Generator'
        assert 'kubernetes' in iac_generator.goal.lower()
        assert iac_generator.allow_delegation == False
    
    def test_validator_initialization(self, mock_config):
        """Test validator agent is properly initialized"""
        from agents import validator
        
        assert validator.role == 'Configuration Validator'
        assert 'validate' in validator.goal.lower()
        assert validator.allow_delegation == False
    
    def test_remediation_agent_initialization(self, mock_config):
        """Test remediation agent is properly initialized"""
        from agents import remediation_agent
        
        assert remediation_agent.role == 'DevOps Remediation Specialist'
        assert 'diagnose' in remediation_agent.goal.lower()
        assert 'failure' in remediation_agent.goal.lower()


class TestAgentBehavior:
    """Test agent execution and response handling"""
    
    def test_agent_with_mocked_llm(self, mock_config):
        """Test agent can work with mocked LLM"""
        from crewai import LLM
        
        mock_llm = LLM(
            model="ollama/llama2:7b",
            base_url="https://test.ollama.cloud",
            api_key="test-key"
        )
        
        test_agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            llm=mock_llm,
            verbose=False,
            allow_delegation=False
        )
        
        assert test_agent.role == "Test Agent"
        assert test_agent.llm is not None
    
    def test_agent_delegation_disabled(self, mock_config):
        """Test that agent delegation is disabled as per project convention"""
        from agents import requirements_analyzer, iac_generator, validator
        
        assert requirements_analyzer.allow_delegation == False
        assert iac_generator.allow_delegation == False
        assert validator.allow_delegation == False


class TestLLMConfiguration:
    """Test LLM wrapper configuration"""
    
    def test_llm_uses_crewai_wrapper(self, mock_config):
        """Test that agents use CrewAI's LLM wrapper, not langchain directly"""
        from agents import llm
        
        # Verify it's a CrewAI LLM instance
        assert isinstance(llm, LLM)
        assert llm.model.startswith("ollama/")
    
    def test_llm_configuration_from_config(self, mock_config):
        """Test LLM is configured from Config class"""
        from agents import llm
        from config import Config
        
        assert Config.OLLAMA_BASE_URL in str(llm.base_url) or Config.OLLAMA_BASE_URL == llm.base_url
        assert llm.api_key == Config.OLLAMA_API_KEY
