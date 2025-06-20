/**
 * Jest setup file for VS Code extension testing
 * Provides mocks for VS Code API and common test utilities
 */

// Mock VS Code API
const mockVSCode = {
  window: {
    showInformationMessage: jest.fn().mockResolvedValue(undefined),
    showErrorMessage: jest.fn().mockResolvedValue(undefined),
    showWarningMessage: jest.fn().mockResolvedValue(undefined),
  },
  commands: {
    registerCommand: jest.fn().mockReturnValue({ dispose: jest.fn() }),
    executeCommand: jest.fn().mockResolvedValue(undefined),
  },
  workspace: {
    getConfiguration: jest.fn().mockReturnValue({
      get: jest.fn(),
      update: jest.fn(),
    }),
  },
  languages: {
    registerHoverProvider: jest.fn().mockReturnValue({ dispose: jest.fn() }),
    registerCodeActionsProvider: jest.fn().mockReturnValue({ dispose: jest.fn() }),
  },
  Uri: {
    file: jest.fn().mockImplementation((path: string) => ({ 
      fsPath: path,
      scheme: 'file',
      path: path 
    })),
    parse: jest.fn(),
  },
  Range: jest.fn().mockImplementation((startLine: number, startChar: number, endLine: number, endChar: number) => ({
    start: { line: startLine, character: startChar },
    end: { line: endLine, character: endChar },
  })),
  Position: jest.fn().mockImplementation((line: number, character: number) => ({
    line,
    character,
  })),
  Disposable: {
    from: jest.fn().mockImplementation((...disposables) => ({
      dispose: () => disposables.forEach((d: any) => d.dispose()),
    })),
  },
};

// Mock the vscode module
jest.mock('vscode', () => mockVSCode, { virtual: true });

// Global test utilities
global.mockVSCode = mockVSCode;

// Reset all mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});

// Increase timeout for integration tests
jest.setTimeout(10000); 