/**
 * Unit tests for extension.ts
 * Tests extension activation, deactivation, and command registration
 */

import { activate, deactivate } from '../extension';
import * as vscode from 'vscode';

// Global mock from setup.ts
declare global {
  var mockVSCode: any;
}

describe('Extension', () => {
  let mockContext: vscode.ExtensionContext;

  beforeEach(() => {
    // Create mock extension context
    mockContext = {
      subscriptions: [],
      workspaceState: {
        get: jest.fn(),
        update: jest.fn(),
      },
      globalState: {
        get: jest.fn(),
        update: jest.fn(),
        setKeysForSync: jest.fn(),
      },
      extensionPath: '/test/path',
      extensionUri: vscode.Uri.file('/test/path'),
      environmentVariableCollection: {} as any,
      extensionMode: 1,
      logUri: vscode.Uri.file('/test/log'),
      storageUri: vscode.Uri.file('/test/storage'),
      globalStorageUri: vscode.Uri.file('/test/globalStorage'),
      secrets: {} as any,
    } as vscode.ExtensionContext;
  });

  describe('activate', () => {
    it('should activate extension and log activation message', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      activate(mockContext);

      expect(consoleSpy).toHaveBeenCalledWith('CodeMentor AI is now active!');
      consoleSpy.mockRestore();
    });

    it('should register enable command', () => {
      activate(mockContext);

      expect(vscode.commands.registerCommand).toHaveBeenCalledWith(
        'codementor.enable',
        expect.any(Function)
      );
    });

    it('should register disable command', () => {
      activate(mockContext);

      expect(vscode.commands.registerCommand).toHaveBeenCalledWith(
        'codementor.disable',
        expect.any(Function)
      );
    });

    it('should add both commands to context subscriptions', () => {
      activate(mockContext);

      expect(mockContext.subscriptions).toHaveLength(2);
    });

    it('should call registerCommand twice (enable and disable)', () => {
      activate(mockContext);

      expect(vscode.commands.registerCommand).toHaveBeenCalledTimes(2);
    });
  });

  describe('command handlers', () => {
    let enableHandler: Function;
    let disableHandler: Function;

    beforeEach(() => {
      activate(mockContext);
      
      // Extract the command handlers from the mock calls
      const registerCommandCalls = (vscode.commands.registerCommand as jest.Mock).mock.calls;
      const enableCall = registerCommandCalls.find(call => call[0] === 'codementor.enable');
      const disableCall = registerCommandCalls.find(call => call[0] === 'codementor.disable');
      
      enableHandler = enableCall?.[1];
      disableHandler = disableCall?.[1];
    });

    it('should show information message when enable command is executed', () => {
      enableHandler();

      expect(vscode.window.showInformationMessage).toHaveBeenCalledWith(
        'CodeMentor AI enabled'
      );
    });

    it('should show information message when disable command is executed', () => {
      disableHandler();

      expect(vscode.window.showInformationMessage).toHaveBeenCalledWith(
        'CodeMentor AI disabled'
      );
    });
  });

  describe('deactivate', () => {
    it('should log deactivation message', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      deactivate();

      expect(consoleSpy).toHaveBeenCalledWith('CodeMentor AI is deactivated');
      consoleSpy.mockRestore();
    });

    it('should not throw any errors', () => {
      expect(() => deactivate()).not.toThrow();
    });
  });

  describe('error handling', () => {
    it('should handle activation errors gracefully', () => {
      // Mock a command registration failure
      (vscode.commands.registerCommand as jest.Mock).mockImplementationOnce(() => {
        throw new Error('Registration failed');
      });

      expect(() => activate(mockContext)).toThrow('Registration failed');
    });
  });
}); 