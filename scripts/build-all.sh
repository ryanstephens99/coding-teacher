#!/bin/bash

# CodeMentor AI Build All Script
set -e

echo "🏗️  Building all CodeMentor AI packages..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
npm run clean

# Build shared package first (dependency for others)
echo "📦 Building shared package..."
cd packages/shared
npm run build
cd ../..

# Build cursor plugin
echo "🔌 Building cursor plugin..."
cd packages/cursor-plugin
npm run build
cd ../..

# Install Python dependencies and run tests for companion app
echo "🐍 Setting up companion app..."
cd packages/companion-app
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    pip install -e .
    echo "✅ Companion app dependencies installed"
else
    echo "❌ Python virtual environment not found. Run './scripts/setup.sh' first."
    exit 1
fi
cd ../..

echo "✅ All packages built successfully!"
echo ""
echo "Next steps:"
echo "  • Run 'npm run dev-start' to start development environment"
echo "  • Or run 'npm run test' to run all tests" 