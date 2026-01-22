"""
Main Orchestrator for CrewAI DevOps Automation
Coordinates agents and tasks to generate Kubernetes manifests from user prompts
"""
import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from crewai import Crew, Process
from agents import requirements_analyzer, iac_generator, validator
from tasks import create_analysis_task, create_generation_task, create_validation_task
from config import Config
import logging

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
# Set console to UTF-8 mode for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
logger = logging.getLogger(__name__)


def check_dependencies():
    """
    Check for required dependencies and provide installation guidance
    Implements self-healing for missing runtime dependencies
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    required_packages = [
        ('crewai', 'crewai'),
        ('dotenv', 'python-dotenv'),
        ('langchain_ollama', 'langchain-ollama')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        logger.error("Missing required dependencies!")
        logger.error("Install with: pip install " + " ".join(missing_packages))
        print("\n⚠️  RUNTIME ERROR: Missing Dependencies")
        print("=" * 80)
        print("\nThe following packages are required but not installed:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n🔧 Self-Healing Recommendation:")
        print(f"   Run: pip install {' '.join(missing_packages)}")
        print("\n" + "=" * 80)
        return False
    
    return True


def install_package(package_name):
    """
    Dynamically install a missing package during runtime
    
    Args:
        package_name (str): Name of the package to install
        
    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        logger.info(f"Attempting to install missing package: {package_name}")
        print(f"\n🔧 Self-Healing: Installing {package_name}...")
        
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name, "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"Successfully installed {package_name}")
        print(f"✅ Successfully installed {package_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package_name}: {e}")
        print(f"❌ Failed to install {package_name}")
        return False


def extract_missing_package(error_message):
    """
    Extract package name from ImportError or ModuleNotFoundError
    
    Args:
        error_message (str): Error message from exception
        
    Returns:
        str: Package name or None
    """
    # Common patterns in import errors
    import re
    
    # Pattern 1: "No module named 'package_name'"
    match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_message)
    if match:
        return match.group(1).split('.')[0]  # Get root package
    
    # Pattern 2: "cannot import name 'X' from 'package'"
    match = re.search(r"from ['\"]([^'\"]+)['\"]", error_message)
    if match:
        return match.group(1).split('.')[0]
    
    return None


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        logger.info(f"Created output directory: {Config.OUTPUT_DIR}")


def save_results(user_prompt, result, execution_time):
    """
    Save execution results to file
    
    Args:
        user_prompt (str): Original user prompt
        result (str): Crew execution result
        execution_time (float): Execution duration in seconds
    """
    ensure_output_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed result as JSON
    result_data = {
        "timestamp": datetime.now().isoformat(),
        "user_prompt": user_prompt,
        "execution_time_seconds": round(execution_time, 2),
        "model": Config.DEFAULT_MODEL,
        "result": str(result)
    }
    
    json_filename = os.path.join(Config.OUTPUT_DIR, f"result_{timestamp}.json")
    with open(json_filename, 'w') as f:
        json.dump(result_data, f, indent=2)
    logger.info(f"Saved detailed results to: {json_filename}")
    
    # Extract and save YAML manifest if present (exact outcome needed)
    result_str = str(result)
    yaml_manifest = None
    
    if "apiVersion" in result_str and "kind:" in result_str:
        yaml_filename = os.path.join(Config.OUTPUT_DIR, f"deployment_{timestamp}.yaml")
        
        # Extract YAML content (simple extraction)
        lines = result_str.split('\n')
        yaml_lines = []
        in_yaml = False
        
        for line in lines:
            if 'apiVersion:' in line:
                in_yaml = True
            if in_yaml:
                yaml_lines.append(line)
        
        if yaml_lines:
            yaml_manifest = '\n'.join(yaml_lines)
            with open(yaml_filename, 'w') as f:
                f.write(yaml_manifest)
            logger.info(f"Saved Kubernetes manifest to: {yaml_filename}")
    
    return json_filename, yaml_manifest


def run_crew(user_prompt):
    """
    Execute the CrewAI workflow
    
    Args:
        user_prompt (str): User's deployment request
        
    Returns:
        str: Execution result
    """
    logger.info("=" * 80)
    logger.info("Starting CrewAI DevOps Automation Workflow")
    logger.info("=" * 80)
    logger.info(f"User Prompt: {user_prompt}")
    
    # Validate configuration
    Config.validate()
    
    # Create tasks with user prompt
    analysis_task = create_analysis_task(user_prompt)
    generation_task = create_generation_task()
    validation_task = create_validation_task()
    
    # Link tasks in sequence
    generation_task.context = [analysis_task]
    validation_task.context = [generation_task]
    
    # Assemble the crew
    crew = Crew(
        agents=[requirements_analyzer, iac_generator, validator],
        tasks=[analysis_task, generation_task, validation_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute with runtime error handling and self-healing
    start_time = datetime.now()
    logger.info("Executing crew workflow...")
    
    max_retries = 3
    retry_count = 0
    result = None
    
    while retry_count < max_retries:
        try:
            result = crew.kickoff()
            break  # Success, exit retry loop
            
        except (ImportError, ModuleNotFoundError) as e:
            logger.warning(f"Runtime import error detected (attempt {retry_count + 1}/{max_retries}): {e}")
            
            # Extract missing package name
            missing_package = extract_missing_package(str(e))
            
            if missing_package:
                print(f"\n⚠️  Runtime Error: Missing dependency '{missing_package}' detected during execution")
                print("=" * 80)
                
                # Attempt to install the missing package
                if install_package(missing_package):
                    retry_count += 1
                    print(f"\n🔄 Retrying crew execution (attempt {retry_count + 1}/{max_retries})...\n")
                    continue
                else:
                    raise Exception(f"Failed to install required package: {missing_package}")
            else:
                # Can't identify the package, re-raise the error
                logger.error(f"Could not identify missing package from error: {e}")
                raise
                
        except Exception as e:
            # Other errors - check if they might be dependency-related
            error_msg = str(e).lower()
            if 'module' in error_msg or 'import' in error_msg:
                logger.warning(f"Possible dependency issue: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    print(f"\n⚠️  Retrying after potential dependency issue (attempt {retry_count + 1}/{max_retries})...")
                    continue
            # Not a dependency issue or max retries reached
            raise
    
    if result is None:
        raise Exception(f"Crew execution failed after {max_retries} attempts")
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    logger.info("=" * 80)
    logger.info("Crew Execution Completed")
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    logger.info("=" * 80)
    
    # Save results and extract exact outcome
    output_file, yaml_manifest = save_results(user_prompt, result, execution_time)
    
    # Return focused output (exact outcome only)
    return {
        'manifest': yaml_manifest,
        'output_file': output_file,
        'execution_time': execution_time,
        'status': 'success' if yaml_manifest else 'no_manifest_generated'
    }


def main():
    """Main entry point with CLI argument support"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='CrewAI DevOps Automation - Kubernetes Manifest Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Deploy a Node.js app with 2 replicas"
  %(prog)s "Deploy Java app with 3 replicas, 512Mi memory, 500m CPU"
  %(prog)s --prompt "Deploy Redis cluster with persistent storage"
        """
    )
    
    parser.add_argument(
        'prompt',
        nargs='*',
        help='Deployment requirements as a natural language prompt'
    )
    
    parser.add_argument(
        '--prompt', '-p',
        dest='prompt_flag',
        help='Alternative way to specify prompt'
    )
    
    parser.add_argument(
        '--output-only',
        action='store_true',
        help='Print only the generated manifest (no logs)'
    )
    
    args = parser.parse_args()
    
    # Determine user prompt from arguments
    if args.prompt_flag:
        user_prompt = args.prompt_flag
    elif args.prompt:
        user_prompt = ' '.join(args.prompt)
    else:
        # Default prompt if none provided
        user_prompt = "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU"
        logger.info("No prompt provided, using default example")
    
    # Check dependencies first (self-healing)
    if not check_dependencies():
        sys.exit(1)
    
    if not args.output_only:
        print("\n" + "=" * 80)
        print("CrewAI DevOps Automation - Kubernetes Manifest Generator")
        print("=" * 80 + "\n")
        print(f"Processing request: {user_prompt}\n")
    
    try:
        result = run_crew(user_prompt)
        
        if args.output_only:
            # Print only the manifest (exact outcome)
            if result['manifest']:
                print(result['manifest'])
            else:
                print("No manifest generated", file=sys.stderr)
                sys.exit(1)
        else:
            # Full output with metadata
            print("\n" + "=" * 80)
            print("EXECUTION COMPLETED")
            print("=" * 80)
            print(f"Status: {result['status']}")
            print(f"Execution Time: {result['execution_time']:.2f} seconds")
            print(f"Output File: {result['output_file']}")
            
            if result['manifest']:
                print("\n" + "=" * 80)
                print("GENERATED MANIFEST (Exact Outcome)")
                print("=" * 80)
                print(result['manifest'])
            else:
                print("\n⚠️  Warning: No valid manifest was generated")
            
            print("\n" + "=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        print(f"\n✗ Error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
