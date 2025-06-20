/**
 * Shared types and interfaces for CodeMentor AI
 */

// Analysis related types
export interface ConventionViolation {
  id: string;
  rule: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  line: number;
  column: number;
  endLine?: number;
  endColumn?: number;
  suggestion?: string;
  reasoning?: string;
  examples?: CodeExample[];
}

export interface CodeExample {
  title: string;
  good?: string;
  bad?: string;
  explanation: string;
}

export interface AnalysisRequest {
  language: string;
  code: string;
  fileName?: string;
  framework?: string;
}

export interface AnalysisResponse {
  violations: ConventionViolation[];
  analysisTime: number;
  language: string;
}

// Communication types
export interface IPCMessage {
  type: string;
  payload: any;
  id?: string;
}

export interface QuestionRequest {
  question: string;
  context?: {
    violation?: ConventionViolation;
    code?: string;
    language?: string;
  };
}

export interface QuestionResponse {
  answer: string;
  confidence: number;
  sources?: string[];
}

// Configuration types
export interface PluginConfig {
  enabled: boolean;
  realTimeAnalysis: boolean;
  supportedLanguages: string[];
  apiEndpoint: string;
  maxViolationsPerFile: number;
}

// Service health types
export interface HealthStatus {
  status: 'healthy' | 'unhealthy' | 'degraded';
  service: string;
  version: string;
  timestamp: string;
  details?: Record<string, any>;
} 