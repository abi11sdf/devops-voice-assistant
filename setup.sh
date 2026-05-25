#!/bin/bash

# AI DevOps Assistant - Automated Setup Script
# This script installs all dependencies and configures the environment

set -e  # Exit on error

echo "======================================"
echo "AI DevOps Assistant - Setup"
echo "======================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Install system dependencies based on OS
echo ""
echo "🖥️  Detecting operating system..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ Detected macOS"
    echo ""
    echo "📦 Installing audio dependencies (requires Homebrew)..."
    if command -v brew &> /dev/null; then
        brew install portaudio
        echo "✅ Audio dependencies installed"
    else
        echo "⚠️  Homebrew not found. Please install portaudio manually:"
        echo "   brew install portaudio"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ Detected Linux"
    echo ""
    echo "📦 Installing audio dependencies..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-pyaudio
        echo "✅ Audio dependencies installed"
    else
        echo "⚠️  apt-get not found. Please install portaudio manually"
    fi
else
    echo "⚠️  Unknown OS. Please install portaudio manually"
fi

# Check AWS CLI
echo ""
echo "☁️  Checking AWS CLI..."
if command -v aws &> /dev/null; then
    aws_version=$(aws --version 2>&1 | awk '{print $1}')
    echo "✅ Found $aws_version"
else
    echo "⚠️  AWS CLI not found"
    echo "   Install from: https://aws.amazon.com/cli/"
fi

# Check kubectl
echo ""
echo "☸️  Checking kubectl..."
if command -v kubectl &> /dev/null; then
    kubectl_version=$(kubectl version --client --short 2>&1 | head -n 1)
    echo "✅ Found $kubectl_version"
else
    echo "⚠️  kubectl not found (optional for Kubernetes operations)"
    echo "   Install from: https://kubernetes.io/docs/tasks/tools/"
fi

# Create .env file if it doesn't exist
echo ""
echo "⚙️  Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env and add your API keys"
else
    echo "✅ .env file already exists"
fi

# Final instructions
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API keys:"
echo "   nano .env"
echo "   (Add your OPENAI_API_KEY)"
echo ""
echo "2. Configure AWS credentials (choose one):"
echo "   Option A: aws configure"
echo "   Option B: Edit .env with AWS keys"
echo ""
echo "3. Test the assistant:"
echo "   python text_assistant.py"
echo ""
echo "4. Run with voice:"
echo "   python ai_devops_assistant.py"
echo ""
echo "For help, see README.md"
echo ""
