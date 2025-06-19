# CM-T1.6: Plugin Activation & Deactivation

## Summary
Implement proper extension lifecycle management including activation, deactivation, and configuration management.

## Acceptance Criteria
- [ ] Extension activates properly on startup
- [ ] Clean deactivation with resource cleanup
- [ ] Configuration management and settings
- [ ] User commands for enable/disable functionality
- [ ] Status reporting and diagnostics
- [ ] Error recovery and graceful degradation

## Implementation Details

### Enhanced Extension Entry Point (src/extension.ts)
```typescript
import * as vscode from 'vscode';
import { ConnectionManager } from './services/connectionManager';
import { DocumentWatcher, DocumentChange } from './services/documentWatcher';
import { CodeExtractor } from './services/codeExtractor';
import { MessageService, AnalysisResponse } from './services/messageService';

// Global state
let connectionManager: ConnectionManager;
let documentWatcher: DocumentWatcher;
let codeExtractor: CodeExtractor;
let messageService: MessageService;
let isCodeMentorEnabled = true;
let statusBarItem: vscode.StatusBarItem;

export async function activate(context: vscode.ExtensionContext) {
    console.log('CodeMentor AI is activating...');

    try {
        // Initialize configuration
        await initializeConfiguration(context);

        // Initialize core services
        await initializeServices(context);

        // Register commands
        registerCommands(context);

        // Setup status bar
        setupStatusBar(context);

        // Start services if enabled
        if (isCodeMentorEnabled) {
            await startServices();
        }

        console.log('CodeMentor AI activated successfully!');
        
        // Show welcome message on first install
        const isFirstInstall = context.globalState.get('codementor.firstInstall', true);
        if (isFirstInstall) {
            await showWelcomeMessage(context);
            context.globalState.update('codementor.firstInstall', false);
        }

    } catch (error) {
        console.error('Failed to activate CodeMentor AI:', error);
        vscode.window.showErrorMessage(`CodeMentor AI activation failed: ${error.message}`);
        
        // Attempt graceful degradation
        await gracefulDegradation(context);
    }
}

async function initializeConfiguration(context: vscode.ExtensionContext): Promise<void> {
    const config = vscode.workspace.getConfiguration('codementor');
    
    // Load user preferences
    isCodeMentorEnabled = config.get('enabled', true);
    
    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(async (e) => {
            if (e.affectsConfiguration('codementor')) {
                await handleConfigurationChange();
            }
        })
    );
}

async function initializeServices(context: vscode.ExtensionContext): Promise<void> {
    // Initialize services in dependency order
    connectionManager = new ConnectionManager();
    documentWatcher = new DocumentWatcher();
    codeExtractor = new CodeExtractor();
    messageService = new MessageService(connectionManager.getClient());

    // Setup document change handling
    documentWatcher.setChangeCallback(async (change: DocumentChange) => {
        if (isCodeMentorEnabled) {
            await handleDocumentChange(change);
        }
    });

    // Add to disposables for cleanup
    context.subscriptions.push(
        connectionManager,
        documentWatcher
    );
}

function registerCommands(context: vscode.ExtensionContext): void {
    const commands = [
        // Main toggle commands
        vscode.commands.registerCommand('codementor.enable', async () => {
            await enableCodeMentor();
        }),

        vscode.commands.registerCommand('codementor.disable', async () => {
            await disableCodeMentor();
        }),

        vscode.commands.registerCommand('codementor.toggle', async () => {
            if (isCodeMentorEnabled) {
                await disableCodeMentor();
            } else {
                await enableCodeMentor();
            }
        }),

        // Diagnostic commands
        vscode.commands.registerCommand('codementor.showStatus', () => {
            showStatusReport();
        }),

        vscode.commands.registerCommand('codementor.reconnect', async () => {
            await reconnectServices();
        }),

        vscode.commands.registerCommand('codementor.analyzeCurrentFile', async () => {
            await analyzeCurrentFile();
        }),

        // Configuration commands
        vscode.commands.registerCommand('codementor.openSettings', () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'codementor');
        }),

        // Internal command handlers
        vscode.commands.registerCommand('codementor.onAnalysisResult', (response: AnalysisResponse) => {
            handleAnalysisResults(response);
        })
    ];

    context.subscriptions.push(...commands);
}

function setupStatusBar(context: vscode.ExtensionContext): void {
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    
    statusBarItem.command = 'codementor.showStatus';
    statusBarItem.show();
    updateStatusBar();
    
    context.subscriptions.push(statusBarItem);
}

async function startServices(): Promise<void> {
    try {
        console.log('Starting CodeMentor services...');
        
        // Initialize connection to companion app
        await connectionManager.initialize();
        
        // Start document watching
        // DocumentWatcher starts automatically on construction
        
        updateStatusBar();
        
        vscode.window.showInformationMessage('CodeMentor AI is now active');
        
    } catch (error) {
        console.error('Failed to start services:', error);
        vscode.window.showErrorMessage(`Failed to start CodeMentor services: ${error.message}`);
        throw error;
    }
}

async function stopServices(): Promise<void> {
    try {
        console.log('Stopping CodeMentor services...');
        
        // Cancel any pending requests
        messageService?.cancelPendingRequests();
        
        // Disconnect from companion app
        connectionManager?.getClient()?.disconnect();
        
        updateStatusBar();
        
        vscode.window.showInformationMessage('CodeMentor AI is now disabled');
        
    } catch (error) {
        console.error('Error stopping services:', error);
    }
}

async function enableCodeMentor(): Promise<void> {
    if (isCodeMentorEnabled) {
        vscode.window.showInformationMessage('CodeMentor AI is already enabled');
        return;
    }

    isCodeMentorEnabled = true;
    
    // Update configuration
    const config = vscode.workspace.getConfiguration('codementor');
    await config.update('enabled', true, vscode.ConfigurationTarget.Global);
    
    await startServices();
}

async function disableCodeMentor(): Promise<void> {
    if (!isCodeMentorEnabled) {
        vscode.window.showInformationMessage('CodeMentor AI is already disabled');
        return;
    }

    isCodeMentorEnabled = false;
    
    // Update configuration
    const config = vscode.workspace.getConfiguration('codementor');
    await config.update('enabled', false, vscode.ConfigurationTarget.Global);
    
    await stopServices();
}

async function handleConfigurationChange(): Promise<void> {
    const config = vscode.workspace.getConfiguration('codementor');
    const newEnabled = config.get('enabled', true);
    
    if (newEnabled !== isCodeMentorEnabled) {
        if (newEnabled) {
            await enableCodeMentor();
        } else {
            await disableCodeMentor();
        }
    }
}

function updateStatusBar(): void {
    if (!statusBarItem) return;

    const client = connectionManager?.getClient();
    const isConnected = client?.getConnectionStatus() ?? false;
    
    if (!isCodeMentorEnabled) {
        statusBarItem.text = "$(circle-slash) CodeMentor";
        statusBarItem.tooltip = "CodeMentor AI (Disabled)";
        statusBarItem.color = new vscode.ThemeColor('disabledForeground');
    } else if (isConnected) {
        statusBarItem.text = "$(check) CodeMentor";
        statusBarItem.tooltip = "CodeMentor AI (Connected)";
        statusBarItem.color = undefined;
    } else {
        statusBarItem.text = "$(warning) CodeMentor";
        statusBarItem.tooltip = "CodeMentor AI (Disconnected)";
        statusBarItem.color = new vscode.ThemeColor('errorForeground');
    }
}

function showStatusReport(): void {
    const client = connectionManager?.getClient();
    const isConnected = client?.getConnectionStatus() ?? false;
    const pendingRequests = messageService?.getPendingRequestCount() ?? 0;
    
    const statusReport = [
        `CodeMentor AI Status Report`,
        ``,
        `Enabled: ${isCodeMentorEnabled ? 'Yes' : 'No'}`,
        `Connected: ${isConnected ? 'Yes' : 'No'}`,
        `Pending Requests: ${pendingRequests}`,
        ``,
        `Services:`,
        `  - Connection Manager: ${connectionManager ? 'Initialized' : 'Not initialized'}`,
        `  - Document Watcher: ${documentWatcher ? 'Active' : 'Inactive'}`,
        `  - Code Extractor: ${codeExtractor ? 'Ready' : 'Not ready'}`,
        `  - Message Service: ${messageService ? 'Ready' : 'Not ready'}`
    ].join('\n');

    vscode.window.showInformationMessage(statusReport, { modal: true });
}

async function reconnectServices(): Promise<void> {
    try {
        vscode.window.showInformationMessage('Reconnecting to companion app...');
        
        // Disconnect first
        connectionManager?.getClient()?.disconnect();
        
        // Wait a moment
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Reconnect
        await connectionManager?.initialize();
        
        updateStatusBar();
        
    } catch (error) {
        vscode.window.showErrorMessage(`Reconnection failed: ${error.message}`);
    }
}

async function analyzeCurrentFile(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active file to analyze');
        return;
    }

    if (!isCodeMentorEnabled) {
        vscode.window.showWarningMessage('CodeMentor AI is disabled');
        return;
    }

    try {
        const document = editor.document;
        const snippets = codeExtractor.extractSnippets({
            document,
            changes: [], // Empty for full file analysis
            timestamp: Date.now(),
            language: document.languageId,
            uri: document.uri.toString()
        });

        if (snippets.length === 0) {
            vscode.window.showInformationMessage('No code to analyze in current file');
            return;
        }

        vscode.window.showInformationMessage('Analyzing current file...');

        const response = await messageService.sendAnalysisRequest(
            snippets,
            {
                uri: document.uri.toString(),
                language: document.languageId,
                timestamp: Date.now()
            },
            'high' // High priority for manual analysis
        );

        await handleAnalysisResults(response);

    } catch (error) {
        vscode.window.showErrorMessage(`Analysis failed: ${error.message}`);
    }
}

async function showWelcomeMessage(context: vscode.ExtensionContext): Promise<void> {
    const action = await vscode.window.showInformationMessage(
        'Welcome to CodeMentor AI! Would you like to see the settings?',
        'Open Settings',
        'Not Now'
    );

    if (action === 'Open Settings') {
        vscode.commands.executeCommand('codementor.openSettings');
    }
}

async function gracefulDegradation(context: vscode.ExtensionContext): Promise<void> {
    // Disable services but keep basic functionality
    isCodeMentorEnabled = false;
    updateStatusBar();
    
    // Register minimal commands for recovery
    const recoveryCommand = vscode.commands.registerCommand('codementor.recover', async () => {
        vscode.window.showInformationMessage('Attempting to recover CodeMentor AI...');
        try {
            await initializeServices(context);
            await enableCodeMentor();
        } catch (error) {
            vscode.window.showErrorMessage(`Recovery failed: ${error.message}`);
        }
    });
    
    context.subscriptions.push(recoveryCommand);
}

// ... existing handleDocumentChange and handleAnalysisResults functions ...

export function deactivate() {
    console.log('CodeMentor AI is deactivating...');
    
    try {
        // Cancel pending operations
        messageService?.cancelPendingRequests();
        
        // Disconnect services
        connectionManager?.dispose();
        documentWatcher?.dispose();
        
        // Clean up status bar
        statusBarItem?.dispose();
        
        console.log('CodeMentor AI deactivated successfully');
        
    } catch (error) {
        console.error('Error during deactivation:', error);
    }
}
```

### Configuration Schema (package.json updates)
```json
{
  "contributes": {
    "configuration": {
      "title": "CodeMentor AI",
      "properties": {
        "codementor.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable/disable CodeMentor AI analysis"
        },
        "codementor.companionApp.host": {
          "type": "string",
          "default": "localhost",
          "description": "Companion app host address"
        },
        "codementor.companionApp.port": {
          "type": "integer",
          "default": 8765,
          "description": "Companion app port"
        },
        "codementor.analysis.debounceDelay": {
          "type": "integer",
          "default": 500,
          "description": "Delay in milliseconds before triggering analysis"
        },
        "codementor.analysis.maxFileSize": {
          "type": "integer",
          "default": 100000,
          "description": "Maximum file size in characters for analysis"
        }
      }
    },
    "commands": [
      {
        "command": "codementor.enable",
        "title": "Enable CodeMentor AI",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.disable",
        "title": "Disable CodeMentor AI",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.toggle",
        "title": "Toggle CodeMentor AI",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.showStatus",
        "title": "Show Status",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.reconnect",
        "title": "Reconnect to Companion App",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.analyzeCurrentFile",
        "title": "Analyze Current File",
        "category": "CodeMentor"
      },
      {
        "command": "codementor.openSettings",
        "title": "Open Settings",
        "category": "CodeMentor"
      }
    ],
    "keybindings": [
      {
        "command": "codementor.toggle",
        "key": "ctrl+shift+m",
        "mac": "cmd+shift+m"
      },
      {
        "command": "codementor.analyzeCurrentFile",
        "key": "ctrl+shift+a",
        "mac": "cmd+shift+a"
      }
    ]
  }
}
```

## Technical Notes
- Implement graceful degradation for error scenarios
- Provide comprehensive user commands and shortcuts
- Support configuration persistence across sessions
- Include diagnostic tools for troubleshooting
- Follow VS Code extension best practices for lifecycle management

## Dependencies
- All previous Epic 1 tickets
- VS Code Extension API
- Configuration system

## Testing
- Extension activates/deactivates cleanly
- Configuration changes applied correctly
- Commands work as expected
- Error scenarios handled gracefully
- Status reporting accurate

## Estimated Hours
4-6 hours 