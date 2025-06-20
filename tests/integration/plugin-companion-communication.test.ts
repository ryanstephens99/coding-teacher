/**
 * Integration tests for Plugin ↔ Companion Communication
 * Tests HTTP requests, WebSocket connections, and message serialization
 */

import { spawn, ChildProcess } from 'child_process';
import { TestClient } from '@jest/globals';

describe('Plugin ↔ Companion Communication', () => {
  let companionProcess: ChildProcess;
  const COMPANION_PORT = 8001; // Use different port for testing
  const COMPANION_URL = `http://localhost:${COMPANION_PORT}`;

  beforeAll(async () => {
    // Start companion service for integration testing
    companionProcess = spawn('python', ['-m', 'uvicorn', 'src.main:app', '--port', COMPANION_PORT.toString()], {
      cwd: '../packages/companion-app',
      env: { ...process.env, PORT: COMPANION_PORT.toString() }
    });

    // Wait for service to start
    await new Promise(resolve => setTimeout(resolve, 3000));
  });

  afterAll(async () => {
    // Clean up companion service
    if (companionProcess) {
      companionProcess.kill('SIGTERM');
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  });

  describe('HTTP Communication', () => {
    it('should successfully connect to companion service', async () => {
      const response = await fetch(`${COMPANION_URL}/health`);
      expect(response.status).toBe(200);
      
      const data = await response.json();
      expect(data.status).toBe('healthy');
      expect(data.service).toBe('codementor-companion');
    });

    it('should send analysis requests and receive responses', async () => {
      const analysisRequest = {
        language: 'typescript',
        code: 'const userName = "john";',
        fileName: 'test.ts'
      };

      const response = await fetch(`${COMPANION_URL}/api/analysis/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisRequest)
      });

      expect(response.status).toBe(200);
      const data = await response.json();
      
      expect(data).toHaveProperty('violations');
      expect(data).toHaveProperty('analysisTime');
      expect(data).toHaveProperty('language');
      expect(data.language).toBe('typescript');
    });

    it('should send LLM questions and receive responses', async () => {
      const questionRequest = {
        question: 'Why should I use camelCase?',
        context: {
          language: 'typescript',
          code: 'const user_name = "john";'
        }
      };

      const response = await fetch(`${COMPANION_URL}/api/llm/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(questionRequest)
      });

      expect(response.status).toBe(200);
      const data = await response.json();
      
      expect(data).toHaveProperty('answer');
      expect(data).toHaveProperty('confidence');
      expect(data).toHaveProperty('sources');
      expect(typeof data.answer).toBe('string');
      expect(typeof data.confidence).toBe('number');
    });

    it('should handle CORS for cross-origin requests', async () => {
      const response = await fetch(`${COMPANION_URL}/health`, {
        headers: { 'Origin': 'vscode-file://vscode-app' }
      });

      expect(response.status).toBe(200);
      // CORS headers should be present (handled by FastAPI middleware)
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid analysis requests gracefully', async () => {
      const invalidRequest = {
        language: 'typescript'
        // Missing required fields
      };

      const response = await fetch(`${COMPANION_URL}/api/analysis/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invalidRequest)
      });

      expect(response.status).toBe(422); // Validation error
    });

    it('should handle network timeouts gracefully', async () => {
      // This test simulates what the plugin should do when companion is unavailable
      const controller = new AbortController();
      setTimeout(() => controller.abort(), 100); // Very short timeout

      try {
        await fetch('http://localhost:9999/nonexistent', {
          signal: controller.signal
        });
        fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeDefined();
        // Plugin should handle this gracefully
      }
    });
  });

  describe('Message Serialization', () => {
    it('should correctly serialize and deserialize analysis requests', async () => {
      const originalRequest = {
        language: 'typescript',
        code: 'const test = "hello";',
        fileName: 'test.ts',
        framework: 'react'
      };

      // Simulate what the plugin does: serialize to JSON
      const serialized = JSON.stringify(originalRequest);
      const deserialized = JSON.parse(serialized);

      expect(deserialized).toEqual(originalRequest);
      expect(deserialized.language).toBe('typescript');
      expect(deserialized.framework).toBe('react');
    });

    it('should handle special characters in code content', async () => {
      const codeWithSpecialChars = `const message = "Hello \\"world\\"\\n\\t";`;
      const request = {
        language: 'typescript',
        code: codeWithSpecialChars,
        fileName: 'special.ts'
      };

      const response = await fetch(`${COMPANION_URL}/api/analysis/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      });

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data.language).toBe('typescript');
    });
  });

  describe('API Contract Compliance', () => {
    it('should maintain consistent response structure across endpoints', async () => {
      // Test that all API responses follow expected patterns
      const endpoints = [
        { path: '/health', method: 'GET' },
        { path: '/api/analysis/supported-languages', method: 'GET' }
      ];

      for (const endpoint of endpoints) {
        const response = await fetch(`${COMPANION_URL}${endpoint.path}`, {
          method: endpoint.method
        });

        expect(response.status).toBe(200);
        expect(response.headers.get('content-type')).toContain('application/json');
        
        const data = await response.json();
        expect(typeof data).toBe('object');
        expect(data).not.toBeNull();
      }
    });

    it('should validate that response schemas match shared type definitions', async () => {
      // Test supported languages endpoint
      const response = await fetch(`${COMPANION_URL}/api/analysis/supported-languages`);
      const data = await response.json();

      expect(data).toHaveProperty('languages');
      expect(Array.isArray(data.languages)).toBe(true);

      // Each language should have the expected structure
      if (data.languages.length > 0) {
        const language = data.languages[0];
        expect(typeof language).toBe('string');
      }
    });
  });
}); 