"""
CrewAI Agent Definitions for DevOps Automation
Defines specialized agents for analyzing requirements and generating IaC scripts
"""
from crewai import Agent
from crewai import LLM
from crewai_tools import FileWriterTool
# from file_tools import write_file, create_dockerfile, save_app_code
from config import Config

# Initialize LLM using CrewAI's LLM wrapper for Ollama
llm = LLM(
    model=f"ollama/{Config.DEFAULT_MODEL}",
    base_url=Config.OLLAMA_BASE_URL,
    api_key=Config.OLLAMA_API_KEY
)

#Initialize File Writer Tool
file_writer_tool = FileWriterTool(
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0   
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

#Developer Agent
app_generator = Agent(
    role = 'Application Code Generator',
    goal='Generate a simple application codebase and dockerfile based on user requirements for testing infrastructure',
    backstory="""You are a skilled software developer with experience in creating simple,
    functional applications in various programming languages. You can quickly generate a codebase
    that meets user requirements, along with a Dockerfile to containerize the application for deployment.
    """,
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0,
    allow_delegation=Config.ALLOW_DELEGATION
)

#Writer Agent
writer_agent = Agent(
    role = 'File Creation Specialist',
    goal='Create and manage application code files and Dockerfiles based on user specifications',
    # tools=[write_file, create_dockerfile, save_app_code],
    tools=[file_writer_tool],
    backstory="""You are an expert in file management and code generation. You excel at creating well-structured 
    application code files and Dockerfiles based on user requirements. You ensure that all files are correctly formatted 
    and ready for deployment in a containerized environment.""",    
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


# Remediation Agent (Self-Healing)
remediation_agent = Agent(
    role='DevOps Remediation Specialist',
    goal='Diagnose deployment failures and propose automated fixes to restore service health',
    backstory="""You are a seasoned Site Reliability Engineer (SRE) with deep expertise 
    in troubleshooting Kubernetes deployments. You can quickly diagnose common failure 
    patterns like OOMKilled pods, CrashLoopBackOff errors, ImagePullBackOff issues, 
    and resource constraints. For each failure, you provide specific remediation actions 
    such as adjusting resource limits, fixing configuration errors, scaling replicas, 
    or suggesting alternative approaches. You think systematically about root causes 
    and prefer permanent fixes over temporary workarounds.""",
    llm=llm,
    verbose=Config.VERBOSE_LEVEL > 0,
    allow_delegation=Config.ALLOW_DELEGATION
)
