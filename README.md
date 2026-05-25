# 🤖 AI DevOps Assistant

A **voice-powered terminal-based AI assistant** for DevOps operations. No frontend required - just speak your commands and the AI executes AWS and Kubernetes operations.

## 🎯 What It Does

```
You: "List my EC2 instances"
AI: *executes boto3 command*
AI: "Found 5 EC2 instances: prod-web-01 is running, staging-db is stopped..."

You: "Restart nginx deployment"  
AI: *executes kubectl rollout restart*
AI: "Successfully restarted deployment nginx"
```

## 🏗️ Architecture

```
Microphone
    ↓
Speech-to-Text (Google Speech Recognition)
    ↓
OpenAI GPT-4 (Tool Calling)
    ↓
boto3 (AWS) / kubectl (Kubernetes)
    ↓
Text-to-Speech (gTTS)
    ↓
Speakers
```

## ✨ Features

### AWS Operations
- ✅ List EC2 instances with states
- ✅ Start/Stop EC2 instances  
- ✅ List S3 buckets
- ✅ Get CloudWatch metrics (CPU usage)

### Kubernetes Operations
- ✅ List pods in any namespace
- ✅ Find failed pods
- ✅ Restart deployments
- ✅ Check deployment status
- ✅ List services
- ✅ Get pod logs

### AI Intelligence
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Automatic tool selection
- ✅ Error handling and explanations

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key** - Get from https://platform.openai.com/api-keys
3. **AWS Credentials** - Configured via `aws configure`
4. **kubectl** (optional) - For Kubernetes operations

### Installation

```bash
# 1. Clone or download the project
cd ai-devops-assistant

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install system dependencies for audio (macOS)
brew install portaudio
pip install PyAudio

# On Ubuntu/Debian:
# sudo apt-get install python3-pyaudio portaudio19-dev
# pip install PyAudio

# On Windows:
# Download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl

# 5. Set environment variables
export OPENAI_API_KEY='sk-your-key-here'

# For AWS (if not already configured)
export AWS_ACCESS_KEY_ID='your-access-key'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
export AWS_DEFAULT_REGION='us-east-1'
```

### Run

```bash
python ai_devops_assistant.py
```

## 📖 Usage Examples

### Voice Commands

Just speak naturally:

```
"List all my EC2 instances"
"Show me failed pods in production namespace"
"What's the CPU usage for instance i-1234567890abcdef0?"
"Restart the nginx deployment"
"Get logs from pod api-server-abc123"
"List all S3 buckets"
"Stop instance i-1234567890abcdef0"
```

### Expected Flow

```
🎤 Listening... (speak now)
📝 You said: list ec2 instances
🤖 Calling OpenAI GPT...
🔧 Executing: list_ec2_instances with args: {}
🔊 AI: I found 3 EC2 instances. The prod-web-01 instance is running with type t3.medium. 
The staging-db instance is stopped with type t2.small. And dev-server is running with type t2.micro.
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# AWS (optional if using aws configure)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=us-east-1

# Kubernetes (optional - uses default kubeconfig)
KUBECONFIG=/path/to/kubeconfig
```

### AWS Setup

```bash
# Option 1: AWS CLI configure
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
export AWS_DEFAULT_REGION='us-east-1'

# Option 3: IAM role (on EC2)
# Automatically uses instance profile
```

### Kubernetes Setup

```bash
# Ensure kubectl is installed and configured
kubectl version --client

# Test connection
kubectl get nodes

# If using multiple clusters
export KUBECONFIG=/path/to/custom/kubeconfig
```

## 🧩 Code Structure

```
ai_devops_assistant.py
├── VoiceEngine          # Speech-to-text and text-to-speech
├── AWSTools             # boto3 AWS operations
├── KubernetesTools      # kubectl Kubernetes operations
└── AIDevOpsAssistant    # Main orchestrator with GPT integration
```

### Adding New Tools

1. **Add function to AWSTools or KubernetesTools:**

```python
def create_s3_bucket(self, bucket_name: str) -> str:
    try:
        self.s3.create_bucket(Bucket=bucket_name)
        return f"Successfully created bucket {bucket_name}"
    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"
```

2. **Register tool in AIDevOpsAssistant.tools:**

```python
{
    "type": "function",
    "function": {
        "name": "create_s3_bucket",
        "description": "Create a new S3 bucket",
        "parameters": {
            "type": "object",
            "properties": {
                "bucket_name": {
                    "type": "string",
                    "description": "Name of the S3 bucket to create"
                }
            },
            "required": ["bucket_name"]
        }
    }
}
```

3. **Add to execute_function:**

```python
elif function_name == "create_s3_bucket":
    return self.aws_tools.create_s3_bucket(arguments['bucket_name'])
```

## 🎓 Learning Path

### Phase 1: Run as-is (Week 1)
- ✅ Get it working
- ✅ Test with your AWS/K8s
- ✅ Understand the flow

### Phase 2: Extend (Week 2-3)
- ➕ Add new AWS services (RDS, Lambda, ECS)
- ➕ Add more K8s operations (scaling, ConfigMaps)
- ➕ Add alerts and notifications

### Phase 3: Production (Week 4+)
- 🔒 Add authentication
- 📊 Add logging and monitoring
- 🐳 Containerize with Docker
- ☁️ Deploy as a service

## 🚫 Text-Only Version (No Voice)

If you don't want voice, create `text_assistant.py`:

```python
from ai_devops_assistant import AIDevOpsAssistant
import os

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    assistant = AIDevOpsAssistant(openai_api_key)
    
    print("AI DevOps Assistant (Text Mode)")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        response = assistant.process_command(user_input)
        print(f"\nAI: {response}\n")

if __name__ == "__main__":
    main()
```

Run with: `python text_assistant.py`

## 🐛 Troubleshooting

### "PyAudio not found"
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### "OpenAI API Key not set"
```bash
export OPENAI_API_KEY='sk-your-key'
```

### "AWS credentials not configured"
```bash
aws configure
# OR
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
```

### "kubectl not found"
```bash
# macOS
brew install kubectl

# Ubuntu
sudo snap install kubectl --classic

# Verify
kubectl version --client
```

### Voice recognition issues
- Speak clearly and not too fast
- Reduce background noise
- Check microphone permissions
- Try adjusting `phrase_time_limit` in `VoiceEngine.listen()`

## 💡 Portfolio Ideas

### For LinkedIn/GitHub

1. **Demo Video**
   - Record yourself using voice commands
   - Show real AWS/K8s operations
   - Highlight AI decision-making

2. **Blog Post**
   - "Building a Voice AI DevOps Assistant"
   - Architecture decisions
   - Lessons learned

3. **Enhancements**
   - Add Slack integration
   - Multi-cloud support (Azure, GCP)
   - Terraform integration
   - Cost optimization suggestions

## 🔒 Security Notes

- **API Keys**: Never commit to Git
- **AWS Credentials**: Use IAM roles when possible
- **Least Privilege**: Create IAM user with minimal permissions
- **Logging**: Review all executed commands
- **Production**: Add approval workflow for destructive operations

## 📊 Cost Estimates

### OpenAI API (GPT-4)
- ~$0.01-0.03 per command
- 100 commands/day = ~$1-3/day

### AWS/K8s
- Read operations: Free
- Write operations: Standard AWS pricing

### Alternative: Use GPT-3.5-turbo
Change model to `gpt-3.5-turbo` in code:
- ~75% cheaper
- Slightly less capable at tool calling

## 🎯 Next Steps

1. **Run it**: Get the basic version working
2. **Customize**: Add your specific tools
3. **Expand**: Web UI, Slack bot, Terraform
4. **Share**: LinkedIn post, GitHub repo, blog
5. **Monetize**: SaaS product, consulting tool

## 📚 Additional Resources

- [OpenAI Function Calling Docs](https://platform.openai.com/docs/guides/function-calling)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [kubectl Commands](https://kubernetes.io/docs/reference/kubectl/)

## 🤝 Contributing

This is a starter template. Fork it, extend it, share improvements!

## 📄 License

MIT License - Use freely for personal and commercial projects

---

**Built for DevOps Engineers who want to combine infrastructure automation with AI**

Made with ❤️ by DevOps enthusiasts
