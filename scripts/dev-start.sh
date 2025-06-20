#!/bin/bash

# CodeMentor AI Development Startup Script
set -e

echo "🚀 Starting CodeMentor AI development environment..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down development servers..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Start companion app in background
echo "🐍 Starting Python companion app..."
cd packages/companion-app
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    python -m src.main &
    COMPANION_PID=$!
    echo "✅ Companion app started (PID: $COMPANION_PID)"
else
    echo "❌ Python virtual environment not found. Run './scripts/setup.sh' first."
    exit 1
fi
cd ../..

# Start shared package build in watch mode
echo "🏗️  Starting shared package watcher..."
cd packages/shared
npm run watch &
SHARED_PID=$!
echo "✅ Shared package watcher started (PID: $SHARED_PID)"
cd ../..

# Start cursor plugin build in watch mode
echo "🔌 Starting cursor plugin watcher..."
cd packages/cursor-plugin
npm run watch &
PLUGIN_PID=$!
echo "✅ Cursor plugin watcher started (PID: $PLUGIN_PID)"
cd ../..

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "Services running:"
echo "  • Companion App: http://localhost:8000"
echo "  • Plugin build watcher: active"
echo "  • Shared package watcher: active"
echo ""
echo "To test the plugin:"
echo "  1. Open packages/cursor-plugin in VS Code"
echo "  2. Press F5 to launch Extension Development Host"
echo ""
echo "Press Ctrl+C to stop all services."

# Wait for all background processes
wait 