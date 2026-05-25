# ⚡ Quick Start Guide

Get the AI DevOps Assistant running in **5 minutes**.

## Prerequisites Check

```bash
# Check Python
python3 --version  # Need 3.8+

# Check AWS (optional)
aws --version

# Check kubectl (optional)
kubectl version --client
```

## Installation (3 steps)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install audio (macOS)
brew install portaudio

# Install audio (Ubuntu)
sudo apt-get install portaudio19-dev python3-pyaudio
```

### 2. Configure API Keys

```bash
# OpenAI API Key (required)
export OPENAI_API_KEY='sk-your-key-here'

# AWS Credentials (optional - if not using aws configure)
export AWS_ACCESS_KEY_ID='your-key'
export AWS_SECRET_ACCESS_KEY='your-secret'
export AWS_DEFAULT_REGION='us-east-1'
```

### 3. Run

```bash
# Text mode (easier to start)
python text_assistant.py

# Voice mode (once working)
python ai_devops_assistant.py
```

## First Commands to Try

```
List my EC2 instances
Show all S3 buckets
List pods in default namespace
Show failed pods
```

## Troubleshooting

### PyAudio error
```bash
# macOS
brew install portaudio && pip install pyaudio

# Ubuntu
sudo apt-get install python3-pyaudio
```

### "OpenAI API key not set"
```bash
export OPENAI_API_KEY='your-key'
```

### "AWS credentials not configured"
```bash
aws configure
```

## Docker Alternative

```bash
# Build
docker-compose build

# Run
docker-compose run --rm ai-devops-assistant
```

## What Next?

1. ✅ **Test basic commands** - EC2, S3, pods
2. ✅ **Add custom tools** - See README "Adding New Tools"
3. ✅ **Create demo video** - LinkedIn/portfolio content
4. ✅ **Extend functionality** - Terraform, monitoring, alerts

## Cost Estimate

- **GPT-4**: ~$0.01-0.03 per command
- **100 commands/day**: ~$1-3/day
- **Use GPT-3.5**: 75% cheaper, change model in code

## Getting Help

- Full documentation: See `README.md`
- Example usage: Run `python demo.py`
- Issues: Check "Troubleshooting" in README

---

**That's it!** You now have a voice AI DevOps assistant.
