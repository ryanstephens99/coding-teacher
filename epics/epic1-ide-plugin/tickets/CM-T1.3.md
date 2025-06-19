# CM-T1.3: Code Document Change Listener

## Summary
Implement real-time file change monitoring within VS Code to detect code modifications and trigger analysis.

## Acceptance Criteria
- [ ] File change listener setup for active documents
- [ ] Debounced change detection to avoid excessive triggers
- [ ] Support for multiple programming languages (Python, JavaScript, TypeScript)
- [ ] Filter for relevant file types and ignore non-code files
- [ ] Performance optimization for large files
- [ ] Change event data structure with document context

## Implementation Details

### Document Watcher Service (src/services/documentWatcher.ts)
```typescript
import * as vscode from 'vscode';

export interface DocumentChange {
    document: vscode.TextDocument;
    changes: vscode.TextDocumentContentChangeEvent[];
    timestamp: number;
    language: string;
    uri: string;
}

export class DocumentWatcher {
    private disposables: vscode.Disposable[] = [];
    private debounceTimers: Map<string, NodeJS.Timeout> = new Map();
    private readonly debounceDelay = 500; // ms
    private onChangeCallback?: (change: DocumentChange) => void;

    // Supported file extensions for analysis
    private readonly supportedLanguages = new Set([
        'python', 'javascript', 'typescript', 'javascriptreact', 'typescriptreact',
        'java', 'csharp', 'go', 'rust', 'cpp', 'c'
    ]);

    constructor() {
        this.setupWatchers();
    }

    private setupWatchers(): void {
        // Watch for document changes
        const changeWatcher = vscode.workspace.onDidChangeTextDocument(
            this.onDocumentChanged.bind(this)
        );

        // Watch for document open/close
        const openWatcher = vscode.workspace.onDidOpenTextDocument(
            this.onDocumentOpened.bind(this)
        );

        const closeWatcher = vscode.workspace.onDidCloseTextDocument(
            this.onDocumentClosed.bind(this)
        );

        this.disposables.push(changeWatcher, openWatcher, closeWatcher);
    }

    private onDocumentChanged(event: vscode.TextDocumentChangeEvent): void {
        const document = event.document;
        
        // Filter out unsupported file types
        if (!this.isDocumentSupported(document)) {
            return;
        }

        // Cancel existing debounce timer for this document
        const existingTimer = this.debounceTimers.get(document.uri.toString());
        if (existingTimer) {
            clearTimeout(existingTimer);
        }

        // Set new debounce timer
        const timer = setTimeout(() => {
            this.processDocumentChange(document, event.contentChanges);
            this.debounceTimers.delete(document.uri.toString());
        }, this.debounceDelay);

        this.debounceTimers.set(document.uri.toString(), timer);
    }

    private processDocumentChange(
        document: vscode.TextDocument,
        changes: readonly vscode.TextDocumentContentChangeEvent[]
    ): void {
        const changeData: DocumentChange = {
            document,
            changes: [...changes],
            timestamp: Date.now(),
            language: document.languageId,
            uri: document.uri.toString()
        };

        console.log(`Document changed: ${document.fileName} (${document.languageId})`);
        
        if (this.onChangeCallback) {
            this.onChangeCallback(changeData);
        }
    }

    private onDocumentOpened(document: vscode.TextDocument): void {
        if (this.isDocumentSupported(document)) {
            console.log(`Document opened: ${document.fileName}`);
            // Could trigger initial analysis here
        }
    }

    private onDocumentClosed(document: vscode.TextDocument): void {
        if (this.isDocumentSupported(document)) {
            console.log(`Document closed: ${document.fileName}`);
            // Clean up any pending timers
            const timer = this.debounceTimers.get(document.uri.toString());
            if (timer) {
                clearTimeout(timer);
                this.debounceTimers.delete(document.uri.toString());
            }
        }
    }

    private isDocumentSupported(document: vscode.TextDocument): boolean {
        // Skip virtual/internal files
        if (document.uri.scheme !== 'file') {
            return false;
        }

        // Check if language is supported
        if (!this.supportedLanguages.has(document.languageId)) {
            return false;
        }

        // Skip very large files (>100KB) for performance
        if (document.getText().length > 100000) {
            return false;
        }

        return true;
    }

    public setChangeCallback(callback: (change: DocumentChange) => void): void {
        this.onChangeCallback = callback;
    }

    public getCurrentActiveDocument(): vscode.TextDocument | undefined {
        return vscode.window.activeTextEditor?.document;
    }

    public getAllOpenDocuments(): vscode.TextDocument[] {
        return vscode.workspace.textDocuments.filter(doc => 
            this.isDocumentSupported(doc)
        );
    }

    public dispose(): void {
        // Clear all timers
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();

        // Dispose all watchers
        this.disposables.forEach(disposable => disposable.dispose());
        this.disposables = [];
    }
}
```

### Integration with Extension (src/extension.ts updates)
```typescript
import * as vscode from 'vscode';
import { ConnectionManager } from './services/connectionManager';
import { DocumentWatcher, DocumentChange } from './services/documentWatcher';

let connectionManager: ConnectionManager;
let documentWatcher: DocumentWatcher;

export function activate(context: vscode.ExtensionContext) {
    console.log('CodeMentor AI is now active!');
    
    // Initialize services
    connectionManager = new ConnectionManager();
    documentWatcher = new DocumentWatcher();

    // Setup document change handling
    documentWatcher.setChangeCallback((change: DocumentChange) => {
        handleDocumentChange(change);
    });

    // Initialize connection
    connectionManager.initialize();

    // Register commands
    const enableCommand = vscode.commands.registerCommand('codementor.enable', () => {
        vscode.window.showInformationMessage('CodeMentor AI enabled');
    });
    
    const disableCommand = vscode.commands.registerCommand('codementor.disable', () => {
        vscode.window.showInformationMessage('CodeMentor AI disabled');
    });

    context.subscriptions.push(
        enableCommand, 
        disableCommand,
        documentWatcher,
        connectionManager
    );
}

function handleDocumentChange(change: DocumentChange): void {
    console.log(`Processing change in ${change.document.fileName}`);
    
    // TODO: This will be connected to code extraction in next ticket
    const client = connectionManager.getClient();
    if (client.getConnectionStatus()) {
        client.sendMessage('document_changed', {
            uri: change.uri,
            language: change.language,
            timestamp: change.timestamp,
            changeCount: change.changes.length
        });
    }
}

export function deactivate() {
    documentWatcher?.dispose();
    connectionManager?.dispose();
    console.log('CodeMentor AI is deactivated');
}
```

## Technical Notes
- Use debouncing to prevent excessive API calls during rapid typing
- Filter by supported languages to avoid analyzing irrelevant files
- Skip large files to maintain performance
- Use VS Code's built-in file watching for efficiency
- Clean up resources properly on disposal

## Dependencies
- VS Code workspace API
- ConnectionManager from previous ticket
- TypeScript for proper typing

## Testing
- Document changes trigger callback with proper debouncing
- Large files are filtered out automatically
- Unsupported file types are ignored
- Memory leaks are prevented with proper cleanup
- Multiple open documents handled correctly

## Estimated Hours
5-7 hours 