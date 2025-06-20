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
