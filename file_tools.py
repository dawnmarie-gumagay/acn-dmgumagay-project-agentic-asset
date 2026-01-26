from crewai_tools import tool
import os
from datetime import datetime

@tool("WriteFile")
def write_file(filename: str, content: str, folder: str = "outputs") -> str:
    """Write content to a file in the specified folder"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return f"File saved successfully to {filepath}"

@tool("CreateDockerfile")
def create_dockerfile(app_type: str, port: str, content: str) -> str:
    """Create a Dockerfile for the application"""
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", "Dockerfile")
    with open(filepath, 'w') as f:
        f.write(content)
    return f"Dockerfile created at {filepath}"

@tool("SaveAppCode")
def save_app_code(filename: str, code: str, subfolder: str = "app") -> str:
    """Save application source code"""
    folder = os.path.join("outputs", subfolder)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as f:
        f.write(code)
    return f"Code saved to {filepath}"