#!/usr/bin/env python3
"""
Minimal AI DevOps Assistant Example
Shows the core concept without voice, just AI + tool calling

This is the simplest version to understand how it works:
1. User types command
2. GPT decides which tool to call
3. Tool executes (AWS/K8s operation)
4. GPT formats the response
"""

import os
import json
from openai import OpenAI
import boto3


def list_ec2_instances():
    """Simple function to list EC2 instances"""
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'id': instance['InstanceId'],
                'state': instance['State']['Name'],
                'type': instance['InstanceType']
            })
    
    return json.dumps(instances)


def main():
    """Main function - demonstrates AI + tool calling"""
    
    # Get API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        return
    
    client = OpenAI(api_key=openai_api_key)
    
    # Define available tools for GPT
    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_ec2_instances",
                "description": "List all EC2 instances in the AWS account",
                "parameters": {"type": "object", "properties": {}}
            }
        }
    ]
    
    print("\n🤖 Minimal AI DevOps Assistant")
    print("="*50)
    print("Try: 'List my EC2 instances'\n")
    
    # Get user input
    user_input = input("You: ")
    
    # Step 1: Send to GPT with tools
    print("\n🤖 Calling GPT to decide what to do...")
    
    messages = [{"role": "user", "content": user_input}]
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Step 2: If GPT wants to call a tool
    if tool_calls:
        print("🔧 GPT decided to call: list_ec2_instances")
        
        # Add GPT's response to messages
        messages.append(response_message)
        
        # Execute the tool
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            
            if function_name == "list_ec2_instances":
                print("⚙️  Executing boto3 command...")
                function_response = list_ec2_instances()
                
                # Add tool result to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })
        
        # Step 3: Get final response from GPT
        print("🤖 Getting formatted response from GPT...")
        
        final_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages
        )
        
        final_message = final_response.choices[0].message.content
        print(f"\n🤖 AI: {final_message}\n")
    
    else:
        # Direct response without tools
        print(f"\n🤖 AI: {response_message.content}\n")


if __name__ == "__main__":
    main()


"""
EXPLANATION OF WHAT HAPPENS:

User types: "List my EC2 instances"

↓

GPT receives the message + list of available tools

↓

GPT decides: "I should call list_ec2_instances()"

↓

Python executes: boto3.client('ec2').describe_instances()

↓

Result sent back to GPT: [{'id': 'i-123', 'state': 'running'}, ...]

↓

GPT formats response: "You have 3 EC2 instances. Instance i-123 is running..."

↓

User sees the formatted response


KEY INSIGHT:
- GPT doesn't execute AWS commands
- GPT just decides WHICH tool to call
- Python executes the actual boto3/kubectl commands
- GPT formats the results nicely

This is called "Function Calling" or "Tool Use"
"""
