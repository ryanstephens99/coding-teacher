# CM-T1.1: Plugin Project Setup (TypeScript)

## Summary
Initialize TypeScript-based VS Code extension project with modern tooling and structure.

## Acceptance Criteria
- [ ] Extension project scaffolded using Yeoman generator
- [ ] TypeScript configuration optimized for VS Code extension development
- [ ] Package.json with correct extension manifest structure
- [ ] Development environment setup with debugging support
- [ ] Initial extension.ts with basic activation/deactivation functions
- [ ] ESLint and Prettier configured for code quality

## Implementation Details

### Setup Commands
```bash
npm install -g yo generator-code
yo code

# Choose:
# - New Extension (TypeScript)
# - Name: CodeMentor AI
# - Identifier: codementor-ai
# - Description: Intelligent coding convention teacher
# - Initialize git repository: Yes
# - Bundle source code: No (for development)
# - Package manager: npm
```

### Key Files to Configure

#### package.json Extensions
```json
{
  "name": "codementor-ai",
  "displayName": "CodeMentor AI",
  "description": "Intelligent coding convention teacher",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": ["Education", "Linters"],
  "activationEvents": [
    "onStartupFinished"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "codementor.enable",
        "title": "Enable CodeMentor"
      },
      {
        "command": "codementor.disable", 
        "title": "Disable CodeMentor"
      }
    ]
  }
}
```

#### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "module": "Node16",
    "target": "ES2022",
    "outDir": "out",
    "lib": ["ES2022"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "Node16"
  },
  "exclude": ["node_modules", ".vscode-test"]
}
```

### Extension Entry Point (src/extension.ts)
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('CodeMentor AI is now active!');
    
    // Register commands
    const enableCommand = vscode.commands.registerCommand('codementor.enable', () => {
        vscode.window.showInformationMessage('CodeMentor AI enabled');
    });
    
    const disableCommand = vscode.commands.registerCommand('codementor.disable', () => {
        vscode.window.showInformationMessage('CodeMentor AI disabled');
    });
    
    context.subscriptions.push(enableCommand, disableCommand);
}

export function deactivate() {
    console.log('CodeMentor AI is deactivated');
}
```

## Technical Notes
- Use Node16 module resolution for better compatibility
- Enable strict TypeScript checking for type safety
- Use onStartupFinished activation for better performance
- Follow VS Code extension naming conventions

## Dependencies
- Node.js 18+
- npm 8+
- VS Code 1.80+

## Testing
- Extension can be launched with F5 in debug mode
- Commands appear in Command Palette
- No TypeScript compilation errors
- Extension activates without errors in console

## Estimated Hours
4-6 hours 