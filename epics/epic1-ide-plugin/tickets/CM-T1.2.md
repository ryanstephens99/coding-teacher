# CM-T1.2: Establish IPC Client in Plugin

## Summary
Set up Inter-Process Communication (IPC) client within the VS Code extension to connect with the companion FastAPI service.

## Acceptance Criteria
- [ ] IPC client module created with connection management
- [ ] WebSocket client implementation for real-time communication
- [ ] Automatic reconnection logic for connection failures
- [ ] Connection status tracking and error handling
- [ ] Message serialization/deserialization utilities
- [ ] Basic ping/pong heartbeat mechanism

## Implementation Details

### IPC Client Service (src/services/ipcClient.ts)
```typescript
import * as vscode from 'vscode';
import WebSocket from 'ws';

export interface IPCMessage {
    type: string;
    payload: any;
    timestamp: number;
    id: string;
}

export class IPCClient {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000;
    private isConnected = false;
    private messageQueue: IPCMessage[] = [];

    constructor(private serverUrl: string = 'ws://localhost:8765') {}

    async connect(): Promise<boolean> {
        try {
            this.ws = new WebSocket(this.serverUrl);
            
            this.ws.on('open', () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                console.log('Connected to companion app');
                this.flushMessageQueue();
            });

            this.ws.on('message', (data: string) => {
                this.handleMessage(JSON.parse(data));
            });

            this.ws.on('close', () => {
                this.isConnected = false;
                this.scheduleReconnect();
            });

            this.ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.isConnected = false;
            });

            return true;
        } catch (error) {
            console.error('Failed to connect:', error);
            return false;
        }
    }

    private scheduleReconnect(): void {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                this.reconnectAttempts++;
                console.log(`Reconnection attempt ${this.reconnectAttempts}`);
                this.connect();
            }, this.reconnectDelay * this.reconnectAttempts);
        }
    }

    sendMessage(type: string, payload: any): void {
        const message: IPCMessage = {
            type,
            payload,
            timestamp: Date.now(),
            id: this.generateMessageId()
        };

        if (this.isConnected && this.ws) {
            this.ws.send(JSON.stringify(message));
        } else {
            this.messageQueue.push(message);
        }
    }

    private flushMessageQueue(): void {
        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            if (message) {
                this.ws?.send(JSON.stringify(message));
            }
        }
    }

    private handleMessage(message: IPCMessage): void {
        switch (message.type) {
            case 'ping':
                this.sendMessage('pong', {});
                break;
            case 'analysis_result':
                // Handle analysis results from companion app
                this.onAnalysisResult(message.payload);
                break;
            default:
                console.log('Unknown message type:', message.type);
        }
    }

    private onAnalysisResult(result: any): void {
        // Emit event for other parts of extension to handle
        vscode.commands.executeCommand('codementor.onAnalysisResult', result);
    }

    private generateMessageId(): string {
        return Math.random().toString(36).substring(2, 15);
    }

    disconnect(): void {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.isConnected = false;
    }

    getConnectionStatus(): boolean {
        return this.isConnected;
    }
}
```

### Connection Manager (src/services/connectionManager.ts)
```typescript
import * as vscode from 'vscode';
import { IPCClient } from './ipcClient';

export class ConnectionManager {
    private client: IPCClient;
    private statusBarItem: vscode.StatusBarItem;

    constructor() {
        this.client = new IPCClient();
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right, 
            100
        );
        this.setupStatusBar();
    }

    async initialize(): Promise<void> {
        const connected = await this.client.connect();
        this.updateStatusBar(connected);
        
        if (connected) {
            vscode.window.showInformationMessage('CodeMentor AI connected');
        } else {
            vscode.window.showWarningMessage('CodeMentor AI connection failed');
        }
    }

    private setupStatusBar(): void {
        this.statusBarItem.text = "$(sync~spin) CodeMentor";
        this.statusBarItem.tooltip = "CodeMentor AI Connection Status";
        this.statusBarItem.command = 'codementor.toggleConnection';
        this.statusBarItem.show();
    }

    private updateStatusBar(connected: boolean): void {
        if (connected) {
            this.statusBarItem.text = "$(check) CodeMentor";
            this.statusBarItem.color = undefined;
        } else {
            this.statusBarItem.text = "$(error) CodeMentor";
            this.statusBarItem.color = new vscode.ThemeColor('errorForeground');
        }
    }

    getClient(): IPCClient {
        return this.client;
    }

    dispose(): void {
        this.client.disconnect();
        this.statusBarItem.dispose();
    }
}
```

### Package Dependencies (package.json additions)
```json
{
  "dependencies": {
    "ws": "^8.14.0"
  },
  "devDependencies": {
    "@types/ws": "^8.5.0"
  }
}
```

## Technical Notes
- Use WebSocket for real-time bidirectional communication
- Implement exponential backoff for reconnection attempts
- Queue messages when disconnected to avoid data loss
- Use status bar to show connection state to user
- Handle various message types with extensible pattern

## Dependencies
- Requires companion app WebSocket server (Epic 2)
- ws npm package for WebSocket client
- VS Code extension API

## Testing
- Connection established successfully on startup
- Automatic reconnection after network interruption
- Message queuing works when disconnected
- Status bar reflects current connection state
- Error handling for invalid server responses

## Estimated Hours
6-8 hours 