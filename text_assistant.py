#!/usr/bin/env python3
"""
Text-Based AI DevOps Assistant
Same as voice version but uses text input/output
Easier for development and testing
"""

import os
import sys
from ai_devops_assistant import AIDevOpsAssistant
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Text-based interaction loop"""
    # Get OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize assistant (without voice)
    print("\n🤖 Initializing AI DevOps Assistant (Text Mode)...")
    
    # Create a modified assistant that doesn't use voice
    assistant = AIDevOpsAssistant(openai_api_key)
    
    print("\n" + "="*60)
    print("🤖 AI DevOps Assistant - Text Mode")
    print("="*60)
    print("\nType your commands naturally. Type 'exit' to quit.")
    print("\nExample commands:")
    print("  - List my EC2 instances")
    print("  - Show failed pods in production")
    print("  - Restart nginx deployment")
    print("  - Get CPU metrics for instance i-12345")
    print("\n" + "="*60 + "\n")
    
    # Main interaction loop
    while True:
        try:
            # Get text input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            # Process command
            print("\n🤖 AI: Thinking...")
            response = assistant.process_command(user_input)
            
            # Display response
            print(f"\n🤖 AI: {response}")
            print("\n" + "-"*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...\n")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
