# Epic 1: Core IDE Plugin & Real-time Monitoring Implementation

Foundational integration with Cursor IDE to monitor code changes and communicate with the backend service for real-time convention analysis.

## Completed Tasks

- [ ] None yet - starting fresh implementation

## In Progress Tasks

- [ ] CM-T1.1: Plugin Project Setup (TypeScript)
- [ ] CM-T1.2: Establish IPC Client in Plugin
- [ ] CM-T1.3: Code Document Change Listener
- [ ] CM-T1.4: Basic Code Snippet Extraction
- [ ] CM-T1.5: Send Code to Companion App (Initial)
- [ ] CM-T1.6: Plugin Activation & Deactivation

## Future Tasks

- [ ] Performance optimization for large files
- [ ] Multi-file monitoring support
- [ ] Advanced error recovery mechanisms
- [ ] User preference management
- [ ] Plugin marketplace preparation

## Implementation Plan

### Architecture Overview
The Cursor IDE plugin will be built using the VS Code Extension API (which Cursor extends) in TypeScript. It will establish real-time monitoring of code changes and maintain a persistent connection with the desktop companion app via WebSocket communication.

### Technical Stack
- **Language**: TypeScript 5.x
- **Framework**: VS Code Extension API
- **Build Tools**: webpack, esbuild
- **Communication**: WebSocket client (ws library)
- **Testing**: Jest, VS Code Extension Test Runner
- **Code Quality**: ESLint + Prettier

### Data Flow
1. Document changes detected by VS Code API
2. Code snippets extracted with context
3. Changes debounced and filtered
4. Data sent via WebSocket to companion app
5. Analysis results received and processed
6. UI feedback provided to user

### Performance Considerations
- Debouncing document changes (300ms delay)
- File size limits (>1MB warning)
- Memory-efficient processing
- Connection retry with exponential backoff
- Message queuing for offline scenarios

## Relevant Files

### Core Extension Files
- `src/extension.ts` - Main extension entry point ✅
- `package.json` - Extension manifest and dependencies ✅
- `tsconfig.json` - TypeScript configuration ✅
- `webpack.config.js` - Build configuration ✅

### Service Layer
- `src/services/connectionManager.ts` - Connection lifecycle management ✅
- `src/services/ipcClient.ts` - WebSocket communication client ✅
- `src/services/documentWatcher.ts` - Real-time document monitoring ✅
- `src/services/codeExtractor.ts` - Code content extraction ✅
- `src/services/messageService.ts` - Message protocol handling ✅

### Type Definitions
- `src/types/ipc.ts` - IPC message type definitions ✅
- `src/types/analysis.ts` - Analysis request/response types ✅
- `src/types/extraction.ts` - Code extraction types ✅

### Utilities
- `src/utils/debounce.ts` - Utility functions ✅
- `src/utils/validation.ts` - Content validation ✅
- `src/utils/correlation.ts` - Request correlation utilities ✅

### Lifecycle Management
- `src/lifecycle/pluginManager.ts` - Extension lifecycle management ✅
- `src/lifecycle/resourceManager.ts` - Resource cleanup ✅
- `src/diagnostics/startupDiagnostics.ts` - Startup validation ✅

## Technical Implementation Details

### CM-T1.1: Plugin Project Setup
- Initialize with Yeoman generator (`yo code`)
- Configure TypeScript with strict mode
- Set up webpack bundling with source maps
- Configure ESLint and Prettier
- Create basic extension manifest
- **Estimated Hours**: 4-6 hours

### CM-T1.2: Establish IPC Client
- Implement WebSocket client with ws library
- Add connection retry with exponential backoff
- Create heartbeat ping/pong mechanism
- Handle connection status tracking
- Implement message queue for offline scenarios
- **Estimated Hours**: 6-8 hours

### CM-T1.3: Code Document Change Listener
- Register VS Code document change listeners
- Implement debounced change handling (300ms)
- Add language filtering for supported types
- Track active editor changes
- Create change event data structures
- **Estimated Hours**: 4-6 hours

### CM-T1.4: Basic Code Snippet Extraction
- Extract full document content
- Implement context detection (functions, classes)
- Add file size validation and limits
- Create structured extraction data format
- Handle encoding and memory optimization
- **Estimated Hours**: 6-8 hours

### CM-T1.5: Send Code to Companion App
- Integrate with IPC client for transmission
- Implement request/response correlation
- Add error handling and retry logic
- Create message protocol definitions
- Handle request timeouts and queuing
- **Estimated Hours**: 6-8 hours

### CM-T1.6: Plugin Activation & Deactivation
- Implement proper VS Code lifecycle
- Add resource cleanup on deactivation
- Create startup diagnostics and validation
- Handle activation errors gracefully
- Implement configuration management
- **Estimated Hours**: 6-8 hours

## Dependencies

### External Dependencies
- `ws` - WebSocket client library
- `@types/ws` - TypeScript definitions for ws
- `@types/vscode` - VS Code API types

### Internal Dependencies
- Epic 2 companion app must be running for full functionality
- WebSocket server endpoint (localhost:8765)
- Proper network connectivity

## Testing Strategy

### Unit Tests
- IPC client connection handling
- Document change detection
- Code extraction logic
- Message serialization/deserialization

### Integration Tests
- End-to-end communication with companion app
- Document monitoring with real files
- Error scenarios and recovery

### Performance Tests
- Large file handling
- Memory usage monitoring
- Connection stability under load

## Security Considerations

- Localhost-only communication
- Input validation and sanitization
- Secure WebSocket connections
- Rate limiting for requests
- No sensitive data logging

## Deployment

### Development
- F5 debugging in VS Code
- Hot reload for development
- Extension host testing

### Production
- Package with `vsce package`
- Install via `.vsix` file
- Marketplace preparation (future)

## Success Criteria

- [ ] Extension activates without errors
- [ ] Real-time document monitoring works
- [ ] Successful communication with companion app
- [ ] Code extraction produces valid data
- [ ] Performance acceptable for normal use
- [ ] Proper error handling and recovery
- [ ] Clean deactivation and resource cleanup 