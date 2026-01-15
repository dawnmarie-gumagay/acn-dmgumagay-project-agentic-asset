"""
Demo: Complete Project Generation
Shows the new Claude Code-style capabilities
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main_project_generator import generate_project
from config import Config


def demo_microservices_ecommerce():
    """Demo: Generate a complete e-commerce microservices project"""
    
    print("\n" + "="*80)
    print("🎬 DEMO: Complete E-Commerce Microservices Project")
    print("="*80)
    
    requirements = """
    Create a microservices e-commerce platform with the following services:
    1. User Service - User registration, authentication, profile management
    2. Product Service - Product catalog, inventory management, search
    3. Cart Service - Shopping cart management, cart persistence
    4. Order Service - Order processing, order history, tracking
    5. Payment Service - Payment processing, transaction management
    
    Requirements:
    - Use Istio service mesh for traffic management
    - Implement monitoring with Prometheus and Grafana
    - Add GitHub Actions CI/CD pipeline
    - Include RBAC and network policies for security
    - Support horizontal pod autoscaling
    - Include complete documentation
    """
    
    output_dir = "./demo-output/ecommerce-platform"
    
    print(f"\n📝 Requirements:\n{requirements}")
    print(f"\n📁 Output Directory: {output_dir}")
    print("\n🚀 Starting generation...\n")
    
    try:
        result = generate_project(
            user_requirements=requirements,
            output_dir=output_dir,
            template_type='microservices'
        )
        
        print("\n" + "="*80)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\n📦 Project: {result['project_name']}")
        print(f"📁 Location: {result['output_dir']}")
        print(f"📄 Files Created: {result['summary']['total_files']}")
        print(f"📂 Directories: {result['summary']['total_directories']}")
        print(f"⏱️  Time: {result['execution_time']:.2f} seconds")
        
        print("\n📚 What was generated:")
        print("  ✓ 5 microservices with Dockerfiles and K8s manifests")
        print("  ✓ Istio service mesh configuration")
        print("  ✓ Terraform infrastructure code")
        print("  ✓ GitHub Actions CI/CD pipeline")
        print("  ✓ Prometheus + Grafana monitoring")
        print("  ✓ RBAC and network policies")
        print("  ✓ Complete documentation suite")
        print("  ✓ Deployment and rollback scripts")
        
        print(f"\n🎯 Next Steps:")
        print(f"  1. cd {output_dir}")
        print("  2. Review the generated project structure")
        print("  3. Customize for your specific needs")
        print("  4. Follow docs/deployment.md to deploy")
        
        print("\n" + "="*80)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return None


def demo_simple_api():
    """Demo: Generate a simple API project"""
    
    print("\n" + "="*80)
    print("🎬 DEMO: Simple REST API Project")
    print("="*80)
    
    requirements = """
    Create a simple REST API application with:
    - Node.js backend with Express
    - PostgreSQL database
    - Redis for caching
    - Authentication and authorization
    - Monitoring and logging
    - CI/CD pipeline
    """
    
    output_dir = "./demo-output/simple-api"
    
    print(f"\n📝 Requirements:\n{requirements}")
    print(f"\n📁 Output Directory: {output_dir}")
    print("\n🚀 Starting generation...\n")
    
    try:
        result = generate_project(
            user_requirements=requirements,
            output_dir=output_dir,
            template_type='microservices'
        )
        
        print("\n✅ Simple API project generated successfully!")
        print(f"📁 Location: {result['output_dir']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return None


def show_project_structure(project_dir: str):
    """Display the generated project structure"""
    
    print("\n" + "="*80)
    print("📁 GENERATED PROJECT STRUCTURE")
    print("="*80)
    
    if not os.path.exists(project_dir):
        print(f"❌ Project directory not found: {project_dir}")
        return
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        """Print directory tree"""
        if current_depth >= max_depth:
            return
        
        try:
            entries = sorted(os.listdir(directory))
            dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
            files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
            
            # Print directories first
            for i, d in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                print(f"{prefix}{'└── ' if is_last_dir else '├── '}{d}/")
                
                new_prefix = prefix + ("    " if is_last_dir else "│   ")
                print_tree(
                    os.path.join(directory, d),
                    new_prefix,
                    max_depth,
                    current_depth + 1
                )
            
            # Print files
            for i, f in enumerate(files):
                is_last = i == len(files) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{f}")
                
        except PermissionError:
            pass
    
    print(f"\n{project_dir}/")
    print_tree(project_dir)


def main():
    """Run all demos"""
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Tip: Copy .env.template to .env and add your OLLAMA_API_KEY")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("🌟 Complete DevOps Project Generator - Demo Suite")
    print("="*80)
    print("\nThis demo showcases the new Claude Code-style capabilities")
    print("that generate complete, production-ready DevOps projects.\n")
    
    # Run demos
    demos = [
        ("E-Commerce Microservices Platform", demo_microservices_ecommerce),
        ("Simple REST API", demo_simple_api),
    ]
    
    results = []
    
    for name, demo_func in demos:
        print(f"\n{'='*80}")
        print(f"Running Demo: {name}")
        print(f"{'='*80}")
        
        result = demo_func()
        if result:
            results.append((name, result))
            
            # Show project structure
            if os.path.exists(result['output_dir']):
                show_project_structure(result['output_dir'])
        
        print("\n" + "="*80)
        print(f"✓ Demo '{name}' completed")
        print("="*80)
    
    # Summary
    print("\n" + "="*80)
    print("🎉 ALL DEMOS COMPLETED")
    print("="*80)
    
    for name, result in results:
        print(f"\n✅ {name}")
        print(f"   Location: {result['output_dir']}")
        print(f"   Files: {result['summary']['total_files']}")
        print(f"   Time: {result['execution_time']:.2f}s")
    
    print("\n" + "="*80)
    print("💡 Next Steps:")
    print("   1. Explore the generated projects")
    print("   2. Review the comprehensive documentation")
    print("   3. Customize for your specific needs")
    print("   4. Deploy using the provided scripts")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
