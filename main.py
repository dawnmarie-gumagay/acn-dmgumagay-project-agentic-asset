"""
Main Orchestrator for CrewAI DevOps Automation
Coordinates agents and tasks to generate Kubernetes manifests from user prompts
"""
import os
import json
from datetime import datetime
from crewai import Crew, Process
from agents import requirements_analyzer, iac_generator, validator
from tasks import create_analysis_task, create_generation_task, create_validation_task
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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
    
    # Extract and save YAML manifest if present
    result_str = str(result)
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
            with open(yaml_filename, 'w') as f:
                f.write('\n'.join(yaml_lines))
            logger.info(f"Saved Kubernetes manifest to: {yaml_filename}")
    
    return json_filename


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
        verbose=Config.VERBOSE_LEVEL
    )
    
    # Execute
    start_time = datetime.now()
    logger.info("Executing crew workflow...")
    
    result = crew.kickoff()
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    logger.info("=" * 80)
    logger.info("Crew Execution Completed")
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    logger.info("=" * 80)
    
    # Save results
    output_file = save_results(user_prompt, result, execution_time)
    
    return result, output_file


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("CrewAI DevOps Automation - Kubernetes Manifest Generator")
    print("=" * 80 + "\n")
    
    # Example prompt (can be replaced with CLI input)
    user_prompt = "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU"
    
    print(f"Processing request: {user_prompt}\n")
    
    try:
        result, output_file = run_crew(user_prompt)
        
        print("\n" + "=" * 80)
        print("FINAL RESULT")
        print("=" * 80)
        print(result)
        print("\n" + "=" * 80)
        print(f"Results saved to: {output_file}")
        print("=" * 80 + "\n")
        
    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    main()
