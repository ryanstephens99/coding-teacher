# CM-T1.5: Send Code to Companion App

## Summary
Implement the data transmission layer to send extracted code snippets to the companion app for analysis.

## Acceptance Criteria
- [ ] Reliable message transmission to companion app
- [ ] Proper data serialization and validation
- [ ] Error handling for transmission failures
- [ ] Message queuing for offline scenarios
- [ ] Response handling from companion app
- [ ] Performance optimization for large payloads

## Implementation Details

### Message Service (src/services/messageService.ts)
```typescript
import * as vscode from 'vscode';
import { CodeSnippet } from './codeExtractor';
import { IPCClient } from './ipcClient';

export interface AnalysisRequest {
    id: string;
    snippets: CodeSnippet[];
    document: {
        uri: string;
        language: string;
        timestamp: number;
    };
    priority: 'high' | 'normal' | 'low';
}

export interface AnalysisResponse {
    id: string;
    violations: Violation[];
    suggestions: Suggestion[];
    processingTime: number;
    timestamp: number;
}

export interface Violation {
    type: string;
    severity: 'error' | 'warning' | 'info';
    message: string;
    range: vscode.Range;
    rule: string;
    fixable: boolean;
    suggestedFix?: string;
}

export interface Suggestion {
    type: string;
    message: string;
    range: vscode.Range;
    improvement: string;
    confidence: number;
}

export class MessageService {
    private client: IPCClient;
    private pendingRequests: Map<string, AnalysisRequest> = new Map();
    private responseCallbacks: Map<string, (response: AnalysisResponse) => void> = new Map();
    private requestTimeout = 30000; // 30 seconds
    private maxPayloadSize = 1024 * 1024; // 1MB

    constructor(client: IPCClient) {
        this.client = client;
        this.setupResponseHandling();
    }

    async sendAnalysisRequest(
        snippets: CodeSnippet[], 
        document: { uri: string; language: string; timestamp: number },
        priority: 'high' | 'normal' | 'low' = 'normal'
    ): Promise<AnalysisResponse> {
        const request: AnalysisRequest = {
            id: this.generateRequestId(),
            snippets,
            document,
            priority
        };

        // Validate payload size
        if (!this.validatePayloadSize(request)) {
            throw new Error('Payload too large for transmission');
        }

        // Store request for timeout handling
        this.pendingRequests.set(request.id, request);

        return new Promise((resolve, reject) => {
            // Set up response callback
            this.responseCallbacks.set(request.id, resolve);

            // Set up timeout
            const timeout = setTimeout(() => {
                this.handleRequestTimeout(request.id);
                reject(new Error(`Analysis request ${request.id} timed out`));
            }, this.requestTimeout);

            // Send request
            try {
                this.client.sendMessage('analysis_request', request);
            } catch (error) {
                clearTimeout(timeout);
                this.cleanupRequest(request.id);
                reject(error);
            }
        });
    }

    private setupResponseHandling(): void {
        // This would be called from the main extension activation
        // Register command to handle analysis results
        vscode.commands.registerCommand('codementor.onAnalysisResult', (response: AnalysisResponse) => {
            this.handleAnalysisResponse(response);
        });
    }

    private handleAnalysisResponse(response: AnalysisResponse): void {
        const callback = this.responseCallbacks.get(response.id);
        if (callback) {
            callback(response);
            this.cleanupRequest(response.id);
        } else {
            console.warn(`Received response for unknown request: ${response.id}`);
        }
    }

    private handleRequestTimeout(requestId: string): void {
        console.warn(`Analysis request ${requestId} timed out`);
        this.cleanupRequest(requestId);
    }

    private cleanupRequest(requestId: string): void {
        this.pendingRequests.delete(requestId);
        this.responseCallbacks.delete(requestId);
    }

    private generateRequestId(): string {
        return `req_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
    }

    private validatePayloadSize(request: AnalysisRequest): boolean {
        const serialized = JSON.stringify(request);
        const sizeInBytes = new Blob([serialized]).size;
        
        if (sizeInBytes > this.maxPayloadSize) {
            console.warn(`Payload size ${sizeInBytes} exceeds maximum ${this.maxPayloadSize}`);
            return false;
        }
        
        return true;
    }

    public getPendingRequestCount(): number {
        return this.pendingRequests.size;
    }

    public cancelPendingRequests(): void {
        for (const requestId of this.pendingRequests.keys()) {
            this.cleanupRequest(requestId);
        }
    }
}
```

### Enhanced IPC Client (src/services/ipcClient.ts updates)
```typescript
// Add to existing IPCClient class

export class IPCClient {
    // ... existing code ...
    
    private messageQueue: IPCMessage[] = [];
    private isProcessingQueue = false;
    private maxQueueSize = 100;

    sendMessage(type: string, payload: any): void {
        const message: IPCMessage = {
            type,
            payload,
            timestamp: Date.now(),
            id: this.generateMessageId()
        };

        if (this.isConnected && this.ws) {
            this.sendMessageImmediate(message);
        } else {
            this.queueMessage(message);
        }
    }

    private sendMessageImmediate(message: IPCMessage): void {
        try {
            this.ws?.send(JSON.stringify(message));
            console.log(`Sent message: ${message.type} (${message.id})`);
        } catch (error) {
            console.error('Failed to send message:', error);
            this.queueMessage(message);
        }
    }

    private queueMessage(message: IPCMessage): void {
        if (this.messageQueue.length >= this.maxQueueSize) {
            // Remove oldest message to make room
            this.messageQueue.shift();
            console.warn('Message queue full, dropping oldest message');
        }
        
        this.messageQueue.push(message);
        console.log(`Queued message: ${message.type} (queue size: ${this.messageQueue.length})`);
    }

    private async flushMessageQueue(): Promise<void> {
        if (this.isProcessingQueue || this.messageQueue.length === 0) {
            return;
        }

        this.isProcessingQueue = true;
        console.log(`Flushing ${this.messageQueue.length} queued messages`);

        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            if (message) {
                this.sendMessageImmediate(message);
                // Small delay to avoid overwhelming the connection
                await new Promise(resolve => setTimeout(resolve, 10));
            }
        }

        this.isProcessingQueue = false;
    }

    // Enhanced connection handling
    async connect(): Promise<boolean> {
        try {
            this.ws = new WebSocket(this.serverUrl);
            
            this.ws.on('open', async () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                console.log('Connected to companion app');
                
                // Flush any queued messages
                await this.flushMessageQueue();
            });

            // ... rest of existing connection code ...

            return true;
        } catch (error) {
            console.error('Failed to connect:', error);
            return false;
        }
    }
}
```

### Integration with Extension (src/extension.ts updates)
```typescript
import { MessageService } from './services/messageService';
import { CodeExtractor, CodeSnippet } from './services/codeExtractor';

let messageService: MessageService;

export function activate(context: vscode.ExtensionContext) {
    // ... existing initialization ...
    
    // Initialize message service
    messageService = new MessageService(connectionManager.getClient());
    
    // Update document change handler
    documentWatcher.setChangeCallback(async (change: DocumentChange) => {
        await handleDocumentChange(change);
    });

    // Register analysis result handler
    const analysisResultHandler = vscode.commands.registerCommand(
        'codementor.onAnalysisResult', 
        (response: AnalysisResponse) => {
            handleAnalysisResults(response);
        }
    );

    context.subscriptions.push(analysisResultHandler);
}

async function handleDocumentChange(change: DocumentChange): Promise<void> {
    try {
        console.log(`Processing change in ${change.document.fileName}`);
        
        // Extract code snippets
        const snippets = codeExtractor.extractSnippets(change);
        
        if (snippets.length === 0) {
            return; // No relevant changes
        }

        // Send to companion app for analysis
        const response = await messageService.sendAnalysisRequest(
            snippets,
            {
                uri: change.uri,
                language: change.language,
                timestamp: change.timestamp
            },
            'normal' // priority
        );

        // Handle the response
        await handleAnalysisResults(response);
        
    } catch (error) {
        console.error('Error processing document change:', error);
        
        // Show user-friendly error message
        if (error.message.includes('timed out')) {
            vscode.window.showWarningMessage(
                'CodeMentor analysis timed out. The companion app may be busy.'
            );
        } else {
            vscode.window.showErrorMessage(
                'CodeMentor analysis failed. Check the connection to the companion app.'
            );
        }
    }
}

async function handleAnalysisResults(response: AnalysisResponse): Promise<void> {
    console.log(`Received analysis results for request ${response.id}`);
    console.log(`Found ${response.violations.length} violations and ${response.suggestions.length} suggestions`);
    
    // TODO: This will be implemented in Epic 4 (Visual Feedback)
    // For now, just log the results
    
    if (response.violations.length > 0) {
        const violationSummary = response.violations
            .map(v => `${v.severity}: ${v.message}`)
            .join('\n');
        
        console.log('Violations found:', violationSummary);
    }
    
    if (response.suggestions.length > 0) {
        const suggestionSummary = response.suggestions
            .map(s => `${s.type}: ${s.message}`)
            .join('\n');
        
        console.log('Suggestions available:', suggestionSummary);
    }
}

export function deactivate() {
    messageService?.cancelPendingRequests();
    // ... existing cleanup ...
}
```

## Technical Notes
- Implement proper message queuing for offline scenarios
- Use request/response correlation with unique IDs
- Add timeout handling for long-running analysis
- Validate payload sizes to prevent transmission issues
- Provide user feedback for connection/analysis issues

## Dependencies
- IPCClient from CM-T1.2
- CodeExtractor from CM-T1.4
- VS Code API for user notifications

## Testing
- Messages sent successfully to companion app
- Request/response correlation works correctly
- Timeout handling prevents hanging requests
- Queue management works during disconnections
- Error scenarios handled gracefully

## Estimated Hours
6-8 hours 