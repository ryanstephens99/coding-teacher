# CodeMentor AI

Intelligent coding convention teacher for Cursor IDE - helping developers learn best practices through real-time feedback and interactive guidance.

## 🏗️ Architecture

CodeMentor AI is built as a monorepo containing two main components:

- **🔌 Cursor IDE Plugin** (`packages/cursor-plugin`) - TypeScript extension providing real-time visual feedback
- **🐍 Companion Service** (`packages/companion-app`) - Python FastAPI service handling code analysis and AI interactions
- **📦 Shared Contracts** (`packages/shared`) - TypeScript types and interfaces shared between components

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm 8+
- Python 3.9+
- VS Code or Cursor IDE

### Setup Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd codementor-ai

# Run setup script (installs all dependencies)
./scripts/setup.sh

# Start development servers
./scripts/dev-start.sh
```

### Testing the Plugin

1. Open `packages/cursor-plugin` in VS Code
2. Press `F5` to launch Extension Development Host
3. The companion service will be running at `http://localhost:8000`

## 📁 Project Structure

```
codementor-ai/
├── packages/
│   ├── cursor-plugin/          # VS Code extension (TypeScript)
│   ├── companion-app/          # Background service (Python)
│   └── shared/                 # Shared types and contracts
├── tools/                      # Build and development tools
├── docs/                       # Architecture and API documentation
├── tests/                      # Integration and performance tests
├── scripts/                    # Development automation scripts
├── epics/                      # Project management and tickets
└── package.json               # Root monorepo configuration
```

## 🛠️ Development Scripts

- `npm run setup` - Initialize development environment
- `npm run dev-start` - Start all development servers
- `npm run build` - Build all packages
- `npm run test` - Run all tests
- `npm run clean` - Clean all build artifacts

## 📚 Documentation

- [Architecture Overview](./docs/architecture/README.md)
- [API Documentation](./docs/api/)
- [Development Guide](./docs/development/)

## 🎯 Features

### Implemented (v0.0.1)
- ✅ Monorepo structure with Lerna
- ✅ VS Code extension scaffold
- ✅ FastAPI companion service scaffold
- ✅ Shared TypeScript contracts
- ✅ Development automation scripts

### In Progress
- 🔄 Real-time code analysis
- 🔄 Convention rule engine
- 🔄 Visual feedback system
- 🔄 Interactive Q&A panel

### Planned
- 📋 Multi-language support
- 📋 Custom rule sets
- 📋 Team collaboration features
- 📋 Performance optimization

## 🤝 Contributing

1. Follow the [Development Guide](./docs/development/)
2. Use conventional commits
3. Ensure all tests pass
4. Update documentation as needed

## 📄 License

MIT - See [LICENSE](./LICENSE) for details