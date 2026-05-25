#!/usr/bin/env python3
"""
Voice AI DevOps Assistant
A terminal-based AI assistant for AWS and Kubernetes operations
No frontend required - uses voice input/output
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Any
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import boto3
from botocore.exceptions import ClientError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceEngine:
    """Handles speech-to-text and text-to-speech"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("🎤 Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self) -> Optional[str]:
        """Capture voice input and convert to text"""
        try:
            with self.microphone as source:
                logger.info("🎤 Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                
            logger.info("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"📝 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("⏱️  No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("❓ Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"❌ Error in speech recognition: {e}")
            return None
    
    def speak(self, text: str):
        """Convert text to speech and play it"""
        try:
            logger.info(f"🔊 AI: {text}")
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play audio
            playsound(temp_file)
            
            # Cleanup
            os.unlink(temp_file)
            
        except Exception as e:
            logger.error(f"❌ Error in text-to-speech: {e}")
            print(f"AI: {text}")  # Fallback to text output


class AWSTools:
    """AWS operations using boto3"""
    
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def list_ec2_instances(self) -> str:
        """List all EC2 instances with their states"""
        try:
            response = self.ec2.describe_instances()
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']
                    state = instance['State']['Name']
                    
                    # Get name tag
                    name = 'N/A'
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                                break
                    
                    instances.append({
                        'id': instance_id,
                        'name': name,
                        'type': instance_type,
                        'state': state
                    })
            
            if not instances:
                return "No EC2 instances found."
            
            result = f"Found {len(instances)} EC2 instances:\n"
            for inst in instances:
                result += f"- {inst['name']} ({inst['id']}): {inst['state']} - {inst['type']}\n"
            
            return result
            
        except ClientError as e:
            return f"AWS Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"Error listing EC2 instances: {str(e)}"
    
    def start_ec2_instance(self, instance_id: str) -> str:
        """Start an EC2 instance"""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            return f"Successfully started EC2 instance {instance_id}"
        except ClientError as e:
            return f"AWS Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"Error starting instance: {str(e)}"
    
    def stop_ec2_instance(self, instance_id: str) -> str:
        """Stop an EC2 instance"""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return f"Successfully stopped EC2 instance {instance_id}"
        except ClientError as e:
            return f"AWS Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"Error stopping instance: {str(e)}"
    
    def list_s3_buckets(self) -> str:
        """List all S3 buckets"""
        try:
            response = self.s3.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            
            if not buckets:
                return "No S3 buckets found."
            
            result = f"Found {len(buckets)} S3 buckets:\n"
            result += "\n".join(f"- {bucket}" for bucket in buckets)
            return result
            
        except ClientError as e:
            return f"AWS Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"Error listing S3 buckets: {str(e)}"
    
    def get_ec2_metrics(self, instance_id: str) -> str:
        """Get CloudWatch metrics for an EC2 instance"""
        try:
            from datetime import datetime, timedelta
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            # Get CPU utilization
            cpu_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            if cpu_response['Datapoints']:
                cpu_avg = cpu_response['Datapoints'][0]['Average']
                return f"EC2 instance {instance_id} - Average CPU utilization (last hour): {cpu_avg:.2f}%"
            else:
                return f"No metrics available for instance {instance_id}"
                
        except ClientError as e:
            return f"AWS Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"Error getting metrics: {str(e)}"


class KubernetesTools:
    """Kubernetes operations using kubectl"""
    
    def execute_kubectl(self, command: List[str]) -> str:
        """Execute kubectl command"""
        try:
            result = subprocess.run(
                ['kubectl'] + command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout or "Command executed successfully"
            else:
                return f"kubectl error: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds"
        except FileNotFoundError:
            return "kubectl not found. Please install kubectl and configure kubeconfig"
        except Exception as e:
            return f"Error executing kubectl: {str(e)}"
    
    def list_pods(self, namespace: str = "default") -> str:
        """List pods in a namespace"""
        output = self.execute_kubectl(['get', 'pods', '-n', namespace])
        return f"Pods in namespace '{namespace}':\n{output}"
    
    def list_failed_pods(self, namespace: str = "default") -> str:
        """List failed pods"""
        output = self.execute_kubectl([
            'get', 'pods', '-n', namespace,
            '--field-selector=status.phase=Failed'
        ])
        return f"Failed pods in namespace '{namespace}':\n{output}"
    
    def restart_deployment(self, deployment_name: str, namespace: str = "default") -> str:
        """Restart a deployment"""
        output = self.execute_kubectl([
            'rollout', 'restart',
            f'deployment/{deployment_name}',
            '-n', namespace
        ])
        return output
    
    def get_deployment_status(self, deployment_name: str, namespace: str = "default") -> str:
        """Get deployment status"""
        output = self.execute_kubectl([
            'rollout', 'status',
            f'deployment/{deployment_name}',
            '-n', namespace
        ])
        return output
    
    def list_services(self, namespace: str = "default") -> str:
        """List services"""
        output = self.execute_kubectl(['get', 'services', '-n', namespace])
        return f"Services in namespace '{namespace}':\n{output}"
    
    def get_pod_logs(self, pod_name: str, namespace: str = "default", tail: int = 50) -> str:
        """Get pod logs"""
        output = self.execute_kubectl([
            'logs', pod_name, '-n', namespace, f'--tail={tail}'
        ])
        return f"Last {tail} lines of logs for pod '{pod_name}':\n{output}"


class AIDevOpsAssistant:
    """Main AI Assistant orchestrator"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.voice = VoiceEngine()
        self.aws_tools = AWSTools()
        self.k8s_tools = KubernetesTools()
        
        # Define available tools for GPT
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_ec2_instances",
                    "description": "List all EC2 instances with their states, names, types",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "start_ec2_instance",
                    "description": "Start an EC2 instance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "instance_id": {
                                "type": "string",
                                "description": "EC2 instance ID (e.g., i-1234567890abcdef0)"
                            }
                        },
                        "required": ["instance_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "stop_ec2_instance",
                    "description": "Stop an EC2 instance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "instance_id": {
                                "type": "string",
                                "description": "EC2 instance ID"
                            }
                        },
                        "required": ["instance_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_s3_buckets",
                    "description": "List all S3 buckets in the AWS account",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_ec2_metrics",
                    "description": "Get CloudWatch metrics (CPU utilization) for an EC2 instance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "instance_id": {
                                "type": "string",
                                "description": "EC2 instance ID"
                            }
                        },
                        "required": ["instance_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_pods",
                    "description": "List all pods in a Kubernetes namespace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_failed_pods",
                    "description": "List failed pods in a Kubernetes namespace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "restart_deployment",
                    "description": "Restart a Kubernetes deployment",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "deployment_name": {
                                "type": "string",
                                "description": "Name of the deployment to restart"
                            },
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            }
                        },
                        "required": ["deployment_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_deployment_status",
                    "description": "Get the status of a Kubernetes deployment",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "deployment_name": {
                                "type": "string",
                                "description": "Name of the deployment"
                            },
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            }
                        },
                        "required": ["deployment_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_services",
                    "description": "List all services in a Kubernetes namespace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_pod_logs",
                    "description": "Get logs from a specific Kubernetes pod",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pod_name": {
                                "type": "string",
                                "description": "Name of the pod"
                            },
                            "namespace": {
                                "type": "string",
                                "description": "Kubernetes namespace (default: default)"
                            },
                            "tail": {
                                "type": "integer",
                                "description": "Number of lines to retrieve (default: 50)"
                            }
                        },
                        "required": ["pod_name"]
                    }
                }
            }
        ]
        
        self.conversation_history = []
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool function"""
        try:
            logger.info(f"🔧 Executing: {function_name} with args: {arguments}")
            
            # AWS Functions
            if function_name == "list_ec2_instances":
                return self.aws_tools.list_ec2_instances()
            elif function_name == "start_ec2_instance":
                return self.aws_tools.start_ec2_instance(arguments['instance_id'])
            elif function_name == "stop_ec2_instance":
                return self.aws_tools.stop_ec2_instance(arguments['instance_id'])
            elif function_name == "list_s3_buckets":
                return self.aws_tools.list_s3_buckets()
            elif function_name == "get_ec2_metrics":
                return self.aws_tools.get_ec2_metrics(arguments['instance_id'])
            
            # Kubernetes Functions
            elif function_name == "list_pods":
                namespace = arguments.get('namespace', 'default')
                return self.k8s_tools.list_pods(namespace)
            elif function_name == "list_failed_pods":
                namespace = arguments.get('namespace', 'default')
                return self.k8s_tools.list_failed_pods(namespace)
            elif function_name == "restart_deployment":
                namespace = arguments.get('namespace', 'default')
                return self.k8s_tools.restart_deployment(
                    arguments['deployment_name'], namespace
                )
            elif function_name == "get_deployment_status":
                namespace = arguments.get('namespace', 'default')
                return self.k8s_tools.get_deployment_status(
                    arguments['deployment_name'], namespace
                )
            elif function_name == "list_services":
                namespace = arguments.get('namespace', 'default')
                return self.k8s_tools.list_services(namespace)
            elif function_name == "get_pod_logs":
                namespace = arguments.get('namespace', 'default')
                tail = arguments.get('tail', 50)
                return self.k8s_tools.get_pod_logs(
                    arguments['pod_name'], namespace, tail
                )
            else:
                return f"Unknown function: {function_name}"
                
        except Exception as e:
            logger.error(f"❌ Error executing {function_name}: {e}")
            return f"Error executing {function_name}: {str(e)}"
    
    def process_command(self, user_input: str) -> str:
        """Process user command through GPT with tool calling"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            logger.info("🤖 Calling OpenAI GPT...")
            
            # Call GPT with tools
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=self.conversation_history,
                tools=self.tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If GPT wants to call tools
            if tool_calls:
                # Add assistant's tool call to history
                self.conversation_history.append(response_message)
                
                # Execute each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the function
                    function_response = self.execute_function(
                        function_name, function_args
                    )
                    
                    # Add function result to history
                    self.conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response
                    })
                
                # Get final response from GPT
                final_response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=self.conversation_history
                )
                
                assistant_message = final_response.choices[0].message.content
            else:
                # Direct response without tools
                assistant_message = response_message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"❌ Error processing command: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def run(self):
        """Main loop - listen for voice commands"""
        print("\n" + "="*60)
        print("🤖 AI DevOps Assistant Started")
        print("="*60)
        print("\nSay 'exit' or 'quit' to stop")
        print("\nExample commands:")
        print("  - List EC2 instances")
        print("  - Show failed pods")
        print("  - Restart nginx deployment")
        print("  - Get CPU usage for instance i-12345")
        print("\n" + "="*60 + "\n")
        
        while True:
            try:
                # Listen for voice input
                user_input = self.voice.listen()
                
                if not user_input:
                    continue
                
                # Check for exit command
                if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
                    self.voice.speak("Goodbye! Shutting down AI DevOps Assistant.")
                    break
                
                # Process command through GPT
                response = self.process_command(user_input)
                
                # Speak the response
                self.voice.speak(response)
                
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                self.voice.speak("Sorry, something went wrong. Please try again.")


def main():
    """Main entry point"""
    # Get OpenAI API key from environment
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
        logger.info("✅ AWS credentials configured")
    except Exception as e:
        logger.warning(f"⚠️  AWS credentials not configured: {e}")
        logger.warning("AWS commands will not work without proper credentials")
    
    # Initialize and run assistant
    assistant = AIDevOpsAssistant(openai_api_key)
    assistant.run()


if __name__ == "__main__":
    main()
