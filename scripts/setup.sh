#!/bin/bash

# CodeMentor AI Development Environment Setup
set -e

echo "🚀 Setting up CodeMentor AI development environment..."

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION is too old. Please install Node.js 18 or higher."
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "❌ Python version $PYTHON_VERSION is too old. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Node.js version: $(node -v)"
echo "✅ Python version: $PYTHON_VERSION"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Bootstrap packages
echo "🔧 Bootstrapping packages..."
npm run bootstrap

# Install Python dependencies for companion app
echo "🐍 Setting up Python companion app..."
cd packages/companion-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../..

# Build shared package
echo "🏗️  Building shared package..."
cd packages/shared
npm run build
cd ../..

echo "✅ Setup complete! Run 'npm run dev-start' to start development servers." 