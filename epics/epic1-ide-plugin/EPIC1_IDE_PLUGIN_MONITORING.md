# Epic 1: Core IDE Plugin & Real-time Monitoring

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

## Implementation Plan

### Architecture Overview
The Cursor IDE plugin will be built using the VS Code Extension API (which Cursor extends) in TypeScript. It will establish real-time monitoring of code changes and maintain a persistent connection with the desktop companion app via WebSocket or HTTP communication.

### Technical Stack
- **Language**: TypeScript
- **Framework**: VS Code Extension API
- **Build Tools**: webpack, esbuild
- **Communication**: WebSocket client (ws library) or HTTP client (axios)
- **Testing**: Jest, VS Code Extension Test Runner

## Detailed Ticket Implementation

### CM-T1.1: Plugin Project Setup (TypeScript)

**Technical Requirements:**
- VS Code Extension Generator (Yeoman)
- TypeScript 5.x configuration
- webpack bundling for production
- ESLint + Prettier for code quality

**Implementation Steps:**
1. Initialize project with `yo code` generator
2. Configure `package.json` with extension metadata:
   ```json
   {
     "name": "codementor-ai",
     "displayName": "CodeMentor AI",
     "description": "Intelligent Convention Teacher",
     "version": "0.1.0",
     "engines": { "vscode": "^1.74.0" },
     "categories": ["Education", "Linters"],
     "activationEvents": ["onStartupFinished"],
     "main": "./out/extension.js"
   }
   ```
3. Set up TypeScript configuration with strict mode
4. Configure webpack for bundling with source maps
5. Set up build scripts: `npm run compile`, `npm run watch`, `npm run package`
6. Create basic extension entry point with activation/deactivation
7. Test "Hello World" command in Cursor IDE

**Files to Create:**
- `src/extension.ts` - Main extension entry point
- `tsconfig.json` - TypeScript configuration
- `webpack.config.js` - Bundling configuration
- `.eslintrc.json` - Linting rules
- `package.json` - Extension manifest

### CM-T1.2: Establish IPC Client in Plugin

**Technical Requirements:**
- WebSocket client library (ws) for real-time communication
- Connection retry logic with exponential backoff
- Heartbeat mechanism for connection health
- Secure local communication (localhost only)

**Implementation Steps:**
1. Install WebSocket client: `npm install ws @types/ws`
2. Create `IPCClient` class with connection management:
   ```typescript
   class IPCClient {
     private ws: WebSocket | null = null;
     private reconnectAttempts = 0;
     private maxReconnectAttempts = 5;
     
     async connect(): Promise<void>
     disconnect(): void
     send(message: any): Promise<void>
     onMessage(handler: (data: any) => void): void
   }
   ```
3. Implement connection retry with exponential backoff
4. Add connection status tracking and events
5. Create message queue for offline scenarios
6. Implement heartbeat ping/pong mechanism
7. Add connection health monitoring

**Files to Create:**
- `src/ipc/IPCClient.ts` - WebSocket client implementation
- `src/ipc/types.ts` - Message type definitions
- `src/ipc/ConnectionManager.ts` - Connection lifecycle management

### CM-T1.3: Code Document Change Listener

**Technical Requirements:**
- VS Code TextDocument API
- TextDocumentChangeEvent handling
- Debouncing for performance optimization
- Language detection capabilities

**Implementation Steps:**
1. Register text document change listeners:
   ```typescript
   vscode.workspace.onDidChangeTextDocument((event) => {
     handleDocumentChange(event);
   });
   ```
2. Implement debounced change handler (300ms delay)
3. Track active editor changes with `onDidChangeActiveTextEditor`
4. Add language filtering for supported languages
5. Implement document state tracking
6. Create change event data structure:
   ```typescript
   interface DocumentChange {
     uri: string;
     languageId: string;
     version: number;
     content: string;
     changes: TextDocumentContentChangeEvent[];
   }
   ```
7. Add performance monitoring for large documents

**Files to Create:**
- `src/document/DocumentMonitor.ts` - Document change tracking
- `src/document/ChangeHandler.ts` - Debounced change processing
- `src/utils/debounce.ts` - Utility functions

### CM-T1.4: Basic Code Snippet Extraction

**Technical Requirements:**
- Full document content extraction
- UTF-8 encoding handling
- Large file size limits (>1MB warning)
- Memory-efficient processing

**Implementation Steps:**
1. Create document content extractor:
   ```typescript
   class CodeExtractor {
     extractFullDocument(document: TextDocument): ExtractedCode
     extractChangedRegions(document: TextDocument, changes: TextDocumentContentChangeEvent[]): ExtractedCode
     validateDocumentSize(document: TextDocument): boolean
   }
   ```
2. Implement content validation and sanitization
3. Add file size limits and warnings
4. Create extracted code data structure:
   ```typescript
   interface ExtractedCode {
     content: string;
     languageId: string;
     uri: string;
     version: number;
     encoding: string;
     metadata: DocumentMetadata;
   }
   ```
5. Add encoding detection and handling
6. Implement memory usage monitoring

**Files to Create:**
- `src/extraction/CodeExtractor.ts` - Content extraction logic
- `src/extraction/types.ts` - Data structures
- `src/utils/validation.ts` - Content validation

### CM-T1.5: Send Code to Companion App (Initial)

**Technical Requirements:**
- Integration with IPCClient from CM-T1.2
- Error handling and retry logic
- Request/response correlation
- Performance monitoring

**Implementation Steps:**
1. Create message protocol definition:
   ```typescript
   interface AnalyzeCodeRequest {
     id: string;
     timestamp: number;
     document: ExtractedCode;
     analysisType: 'full' | 'incremental';
   }
   
   interface AnalyzeCodeResponse {
     id: string;
     success: boolean;
     issues: ConventionIssue[];
     error?: string;
   }
   ```
2. Implement request sender with correlation tracking
3. Add response timeout handling (30 seconds)
4. Create retry logic for failed requests
5. Implement request queuing for offline scenarios
6. Add performance metrics collection
7. Create error reporting mechanism

**Files to Create:**
- `src/communication/MessageProtocol.ts` - Protocol definitions
- `src/communication/RequestManager.ts` - Request/response handling
- `src/utils/correlation.ts` - Request correlation utilities

### CM-T1.6: Plugin Activation & Deactivation

**Technical Requirements:**
- Proper VS Code extension lifecycle
- Resource cleanup on deactivation
- Error handling during startup
- Graceful shutdown procedures

**Implementation Steps:**
1. Implement activation function:
   ```typescript
   export async function activate(context: ExtensionContext): Promise<void> {
     try {
       await initializePlugin(context);
       registerCommands(context);
       startDocumentMonitoring();
       await connectToCompanionApp();
     } catch (error) {
       handleActivationError(error);
     }
   }
   ```
2. Create deactivation cleanup:
   ```typescript
   export async function deactivate(): Promise<void> {
     await cleanupResources();
     disconnectFromCompanionApp();
     disposeEventListeners();
   }
   ```
3. Add error handling for activation failures
4. Implement resource disposal tracking
5. Create startup diagnostics and logging
6. Add configuration validation on startup

**Files to Create:**
- `src/lifecycle/PluginManager.ts` - Lifecycle management
- `src/lifecycle/ResourceManager.ts` - Resource cleanup
- `src/diagnostics/StartupDiagnostics.ts` - Startup validation

## Relevant Files

- `src/extension.ts` - Main extension entry point ✅
- `src/ipc/IPCClient.ts` - WebSocket communication client ✅
- `src/document/DocumentMonitor.ts` - Real-time document monitoring ✅
- `src/extraction/CodeExtractor.ts` - Code content extraction ✅
- `src/communication/MessageProtocol.ts` - IPC message definitions ✅
- `src/lifecycle/PluginManager.ts` - Extension lifecycle management ✅
- `package.json` - Extension manifest and dependencies ✅
- `tsconfig.json` - TypeScript configuration ✅
- `webpack.config.js` - Build configuration ✅

## Technical Considerations

### Performance Optimization
- Implement debouncing for document changes (300ms)
- Add file size limits (1MB threshold)
- Use efficient diff algorithms for large documents
- Implement memory usage monitoring

### Error Handling
- Network connectivity issues
- Companion app unavailability
- Document parsing failures
- Memory constraints

### Security
- Localhost-only communication
- Input validation and sanitization
- Secure WebSocket connections
- Rate limiting for requests

### Testing Strategy
- Unit tests for core functionality
- Integration tests with mock companion app
- Performance tests with large documents
- VS Code extension test framework 