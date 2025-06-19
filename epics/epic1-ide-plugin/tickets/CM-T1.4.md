# CM-T1.4: Basic Code Snippet Extraction

## Summary
Extract relevant code snippets from document changes for analysis by the companion app.

## Acceptance Criteria
- [ ] Code snippet extraction from VS Code documents
- [ ] Language-aware parsing with AST-based extraction
- [ ] Context detection for meaningful code blocks
- [ ] Filtering out irrelevant changes (comments, whitespace)
- [ ] Structured data format for analysis
- [ ] Performance optimization for large files

## Implementation Details

### Code Extractor Service (src/services/codeExtractor.ts)
```typescript
import * as vscode from 'vscode';
import { DocumentChange } from './documentWatcher';

export interface CodeSnippet {
    content: string;
    language: string;
    uri: string;
    range: vscode.Range;
    context: CodeContext;
    timestamp: number;
}

export interface CodeContext {
    functionName?: string;
    className?: string;
    imports?: string[];
    surrounding: string;
    changeType: 'addition' | 'modification' | 'deletion';
}

export class CodeExtractor {
    private readonly maxSnippetSize = 2000; // characters
    private readonly contextLines = 5; // lines before/after change

    extractSnippets(change: DocumentChange): CodeSnippet[] {
        const snippets: CodeSnippet[] = [];
        const document = change.document;

        for (const textChange of change.changes) {
            // Skip empty or whitespace-only changes
            if (this.isIrrelevantChange(textChange)) {
                continue;
            }

            const snippet = this.createSnippet(document, textChange, change);
            if (snippet) {
                snippets.push(snippet);
            }
        }

        return snippets;
    }

    private createSnippet(
        document: vscode.TextDocument,
        textChange: vscode.TextDocumentContentChangeEvent,
        change: DocumentChange
    ): CodeSnippet | null {
        try {
            const range = this.expandRange(document, textChange.range);
            const content = document.getText(range);
            
            // Skip if snippet is too large
            if (content.length > this.maxSnippetSize) {
                return null;
            }

            const context = this.extractContext(document, textChange.range);

            return {
                content,
                language: change.language,
                uri: change.uri,
                range,
                context,
                timestamp: change.timestamp
            };
        } catch (error) {
            console.error('Error creating snippet:', error);
            return null;
        }
    }

    private expandRange(document: vscode.TextDocument, range: vscode.Range): vscode.Range {
        // Expand to include surrounding context
        const startLine = Math.max(0, range.start.line - this.contextLines);
        const endLine = Math.min(
            document.lineCount - 1, 
            range.end.line + this.contextLines
        );

        return new vscode.Range(startLine, 0, endLine, document.lineAt(endLine).text.length);
    }

    private extractContext(document: vscode.TextDocument, range: vscode.Range): CodeContext {
        const context: CodeContext = {
            surrounding: '',
            changeType: 'modification'
        };

        try {
            // Find containing function or class
            const position = range.start;
            const symbols = this.findContainingSymbols(document, position);
            
            if (symbols.function) {
                context.functionName = symbols.function.name;
            }
            
            if (symbols.class) {
                context.className = symbols.class.name;
            }

            // Extract imports from top of file
            context.imports = this.extractImports(document);

            // Get surrounding code for context
            const surroundingRange = this.expandRange(document, range);
            context.surrounding = document.getText(surroundingRange);

        } catch (error) {
            console.error('Error extracting context:', error);
        }

        return context;
    }

    private findContainingSymbols(document: vscode.TextDocument, position: vscode.Position) {
        // This is a simplified version - in practice, you might want to use
        // VS Code's built-in symbol provider or a language-specific parser
        const text = document.getText();
        const lines = text.split('\n');
        
        let currentFunction: string | undefined;
        let currentClass: string | undefined;

        for (let i = position.line; i >= 0; i--) {
            const line = lines[i];
            
            // Look for function definitions
            const functionMatch = line.match(/^\s*(async\s+)?function\s+(\w+)|^\s*(\w+)\s*[=:]\s*(async\s+)?\(/);
            if (functionMatch && !currentFunction) {
                currentFunction = functionMatch[2] || functionMatch[3];
            }

            // Look for class definitions
            const classMatch = line.match(/^\s*class\s+(\w+)/);
            if (classMatch && !currentClass) {
                currentClass = classMatch[1];
            }

            // Stop if we've found both or reached a major scope boundary
            if ((currentFunction && currentClass) || this.isScopeBoundary(line)) {
                break;
            }
        }

        return {
            function: currentFunction ? { name: currentFunction } : undefined,
            class: currentClass ? { name: currentClass } : undefined
        };
    }

    private extractImports(document: vscode.TextDocument): string[] {
        const imports: string[] = [];
        const text = document.getText();
        const lines = text.split('\n');

        // Look at first 50 lines for imports (optimization)
        const maxImportLines = Math.min(50, lines.length);
        
        for (let i = 0; i < maxImportLines; i++) {
            const line = lines[i].trim();
            
            // JavaScript/TypeScript imports
            if (line.startsWith('import ') || line.startsWith('const ') && line.includes('require(')) {
                imports.push(line);
            }
            
            // Python imports
            if (line.startsWith('from ') || line.startsWith('import ')) {
                imports.push(line);
            }

            // Stop at first non-import/non-comment line after imports have started
            if (imports.length > 0 && !this.isImportOrComment(line)) {
                break;
            }
        }

        return imports;
    }

    private isImportOrComment(line: string): boolean {
        const trimmed = line.trim();
        return trimmed === '' || 
               trimmed.startsWith('//') || 
               trimmed.startsWith('#') ||
               trimmed.startsWith('/*') ||
               trimmed.startsWith('*') ||
               trimmed.startsWith('import ') ||
               trimmed.startsWith('from ') ||
               trimmed.startsWith('const ') && trimmed.includes('require(');
    }

    private isScopeBoundary(line: string): boolean {
        const trimmed = line.trim();
        return trimmed.startsWith('export ') || 
               trimmed.startsWith('module.exports') ||
               (trimmed.length > 0 && !trimmed.startsWith(' ') && !trimmed.startsWith('\t'));
    }

    private isIrrelevantChange(change: vscode.TextDocumentContentChangeEvent): boolean {
        const text = change.text.trim();
        
        // Skip empty changes
        if (text === '') {
            return true;
        }

        // Skip pure whitespace changes
        if (/^\s+$/.test(change.text)) {
            return true;
        }

        // Skip single character changes that are likely typos
        if (text.length === 1 && /[a-zA-Z0-9]/.test(text)) {
            return true;
        }

        // Skip comment-only changes
        if (this.isCommentOnly(text)) {
            return true;
        }

        return false;
    }

    private isCommentOnly(text: string): boolean {
        const lines = text.split('\n');
        return lines.every(line => {
            const trimmed = line.trim();
            return trimmed === '' || 
                   trimmed.startsWith('//') || 
                   trimmed.startsWith('#') ||
                   trimmed.startsWith('/*') ||
                   trimmed.startsWith('*');
        });
    }
}
```

### Integration with Document Watcher (src/extension.ts updates)
```typescript
import { CodeExtractor, CodeSnippet } from './services/codeExtractor';

let codeExtractor: CodeExtractor;

export function activate(context: vscode.ExtensionContext) {
    // ... existing code ...
    
    // Initialize code extractor
    codeExtractor = new CodeExtractor();
    
    // Update document change handler
    documentWatcher.setChangeCallback((change: DocumentChange) => {
        handleDocumentChange(change);
    });
}

function handleDocumentChange(change: DocumentChange): void {
    console.log(`Processing change in ${change.document.fileName}`);
    
    // Extract code snippets
    const snippets = codeExtractor.extractSnippets(change);
    
    if (snippets.length === 0) {
        return; // No relevant changes
    }
    
    // Send to companion app
    const client = connectionManager.getClient();
    if (client.getConnectionStatus()) {
        client.sendMessage('code_analysis_request', {
            snippets,
            document: {
                uri: change.uri,
                language: change.language,
                timestamp: change.timestamp
            }
        });
    }
}
```

## Technical Notes
- Use VS Code's symbol providers when available for accurate context detection
- Implement language-specific parsing for better accuracy
- Cache parsed results to improve performance
- Filter out irrelevant changes to reduce noise
- Include sufficient context for meaningful analysis

## Dependencies
- DocumentWatcher from previous ticket
- VS Code API for symbol detection
- ConnectionManager for sending extracted snippets

## Testing
- Code snippets extracted correctly for various languages
- Context detection works for functions and classes
- Import statements captured accurately
- Irrelevant changes filtered out properly
- Performance acceptable for large files

## Estimated Hours
8-10 hours 