"""
CrewAI Agent Definitions for DevOps Automation
Defines specialized agents for analyzing requirements and generating IaC scripts
"""
from crewai import Agent
from crewai import LLM
from config import Config

# Initialize LLM using CrewAI's LLM wrapper for Ollama
llm = LLM(
    model=f"ollama/{Config.DEFAULT_MODEL}",
    base_url=Config.OLLAMA_BASE_URL,
    api_key=Config.OLLAMA_API_KEY
)

# Requirements Analyzer Agent
requirements_analyzer = Agent(
    role='DevOps Requirements Analyst',
    goal='Analyze user requirements and extract deployment specifications for containerized applications',
    backstory="""You are an experienced DevOps engineer who excels at understanding 
    application deployment requirements. You can identify the key components needed 
    for deploying applications on Kubernetes, including resource requirements, 
    container images, ports, and environment configurations.""",
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0,
    allow_delegation=Config.ALLOW_DELEGATION
)

# IaC Generator Agent
iac_generator = Agent(
    role='Infrastructure as Code Generator',
    goal='Generate production-ready Kubernetes deployment manifests based on analyzed requirements',
    backstory="""You are a Kubernetes expert who specializes in writing clean, 
    efficient, and production-ready YAML manifests. You follow best practices for 
    Kubernetes deployments including proper resource limits, health checks, labels, 
    and annotations. You generate valid YAML that can be directly applied to a cluster.""",
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0,
    allow_delegation=Config.ALLOW_DELEGATION
)

# Validator Agent
validator = Agent(
    role='Configuration Validator',
    goal='Validate generated Kubernetes manifests for syntax correctness and best practices',
    backstory="""You are a quality assurance expert for Kubernetes configurations. 
    You review YAML manifests to ensure they are syntactically correct, follow 
    Kubernetes best practices, and include all necessary fields. You provide 
    feedback on potential issues and confirm when configurations are deployment-ready.""",
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0,
    allow_delegation=Config.ALLOW_DELEGATION
)
