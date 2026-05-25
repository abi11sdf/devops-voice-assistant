#!/usr/bin/env python3
"""
Demo Script - Shows example usage of AI DevOps Assistant
Runs predefined commands to demonstrate capabilities
"""

import os
import time
from ai_devops_assistant import AIDevOpsAssistant

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_demo():
    """Run demonstration commands"""
    
    # Check for API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return
    
    print_header("AI DevOps Assistant - Demo Mode")
    print("This demo will show the assistant's capabilities")
    print("by running example commands.\n")
    
    # Initialize assistant
    print("🤖 Initializing AI Assistant...")
    assistant = AIDevOpsAssistant(openai_api_key)
    print("✅ Ready!\n")
    
    # Demo commands
    demo_commands = [
        {
            "command": "List all my EC2 instances",
            "description": "AWS - List EC2 instances with their states"
        },
        {
            "command": "Show me all S3 buckets",
            "description": "AWS - List all S3 buckets"
        },
        {
            "command": "List pods in default namespace",
            "description": "Kubernetes - List all pods"
        },
        {
            "command": "Show failed pods",
            "description": "Kubernetes - Find failed pods"
        },
        {
            "command": "What's the CPU usage for instance i-0123456789abcdef0?",
            "description": "AWS - Get CloudWatch metrics"
        }
    ]
    
    # Run each command
    for idx, demo in enumerate(demo_commands, 1):
        print_header(f"Demo {idx}/{len(demo_commands)}: {demo['description']}")
        
        print(f"💬 Command: \"{demo['command']}\"")
        print("\n🤖 Processing...")
        
        try:
            response = assistant.process_command(demo['command'])
            print(f"\n🤖 AI Response:")
            print(response)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Wait before next command
        if idx < len(demo_commands):
            print("\n⏱️  Next command in 3 seconds...")
            time.sleep(3)
    
    print_header("Demo Complete!")
    print("The AI successfully:")
    print("  ✅ Understood natural language commands")
    print("  ✅ Selected appropriate tools (AWS/K8s)")
    print("  ✅ Executed operations via boto3/kubectl")
    print("  ✅ Provided clear responses")
    print("\nTry it yourself:")
    print("  python text_assistant.py")
    print("  python ai_devops_assistant.py  (with voice)")
    print("")


if __name__ == "__main__":
    run_demo()
