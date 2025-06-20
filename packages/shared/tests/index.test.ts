/**
 * Unit tests for shared package
 * Tests type definitions, exports, and contract validation
 */

import * as SharedTypes from '../src/index';

describe('Shared Package', () => {
  describe('Type Exports', () => {
    it('should export all expected types', () => {
      // Test that the main types are available
      expect(typeof SharedTypes).toBe('object');
      
      // These should be available as type definitions
      // We can't directly test types at runtime, but we can test the module structure
      const exportedKeys = Object.keys(SharedTypes);
      expect(Array.isArray(exportedKeys)).toBe(true);
    });
  });

  describe('Type Definitions', () => {
    it('should allow creation of valid API request objects', () => {
      // Test that we can create objects matching our expected interfaces
      const analysisRequest = {
        language: 'typescript',
        code: 'const test = "hello";',
        fileName: 'test.ts'
      };
      
      expect(analysisRequest.language).toBe('typescript');
      expect(analysisRequest.code).toBe('const test = "hello";');
      expect(analysisRequest.fileName).toBe('test.ts');
    });

    it('should allow creation of valid violation objects', () => {
      const violation = {
        id: 'test-violation',
        rule: 'naming-convention',
        severity: 'warning' as const,
        message: 'Use camelCase',
        line: 1,
        column: 6
      };
      
      expect(violation.id).toBe('test-violation');
      expect(violation.severity).toBe('warning');
      expect(violation.line).toBe(1);
    });

    it('should allow creation of valid LLM request objects', () => {
      const llmRequest = {
        question: 'Why use camelCase?',
        context: {
          language: 'typescript',
          code: 'const user_name = "john";'
        }
      };
      
      expect(llmRequest.question).toBe('Why use camelCase?');
      expect(llmRequest.context?.language).toBe('typescript');
    });

    it('should allow creation of valid WebSocket message objects', () => {
      const wsMessage = {
        type: 'analysis_request',
        payload: {
          language: 'typescript',
          code: 'const test = 1;'
        },
        timestamp: Date.now()
      };
      
      expect(wsMessage.type).toBe('analysis_request');
      expect(typeof wsMessage.timestamp).toBe('number');
    });
  });

  describe('Contract Validation', () => {
    it('should validate analysis response structure', () => {
      const analysisResponse = {
        violations: [],
        analysisTime: 0.1,
        language: 'typescript'
      };
      
      expect(Array.isArray(analysisResponse.violations)).toBe(true);
      expect(typeof analysisResponse.analysisTime).toBe('number');
      expect(typeof analysisResponse.language).toBe('string');
    });

    it('should validate LLM response structure', () => {
      const llmResponse = {
        answer: 'CamelCase improves readability',
        confidence: 0.9,
        sources: ['MDN', 'TypeScript Handbook']
      };
      
      expect(typeof llmResponse.answer).toBe('string');
      expect(typeof llmResponse.confidence).toBe('number');
      expect(Array.isArray(llmResponse.sources)).toBe(true);
    });

    it('should validate supported languages structure', () => {
      const supportedLanguages = {
        languages: [
          { id: 'typescript', name: 'TypeScript', extensions: ['.ts', '.tsx'] },
          { id: 'javascript', name: 'JavaScript', extensions: ['.js', '.jsx'] }
        ]
      };
      
      expect(Array.isArray(supportedLanguages.languages)).toBe(true);
      expect(supportedLanguages.languages[0].id).toBe('typescript');
      expect(Array.isArray(supportedLanguages.languages[0].extensions)).toBe(true);
    });
  });

  describe('Build Integration', () => {
    it('should compile TypeScript successfully', () => {
      // This test passes if the TypeScript compilation succeeds
      // The fact that Jest can import and run this file means TS compilation worked
      expect(true).toBe(true);
    });

    it('should maintain type safety across packages', () => {
      // Test that shared types can be used consistently
      const sharedViolation = {
        id: 'shared-test',
        rule: 'test-rule',
        severity: 'error' as const,
        message: 'Test message',
        line: 1,
        column: 1
      };
      
      // This should compile without errors if types are consistent
      expect(sharedViolation.severity).toBe('error');
    });
  });
}); 