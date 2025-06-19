# Epic 1: Core IDE Plugin & Real-time Monitoring

## Overview
Enable CodeMentor AI to listen to code changes in Cursor and communicate with the backend service.

## Goal
Create a VS Code extension that can monitor file changes, extract code snippets, and establish real-time communication with the companion app service.

## Key Technologies
- TypeScript
- VS Code Extension API  
- WebSocket/IPC
- Node.js

## Dependencies
- None (foundational epic)

## Estimated Effort
2-3 weeks

## Tickets
1. [CM-T1.1: Plugin Project Setup](./tickets/CM-T1.1.md) - Initialize TypeScript extension project
2. [CM-T1.2: Establish IPC Client](./tickets/CM-T1.2.md) - Set up communication channel
3. [CM-T1.3: Code Document Change Listener](./tickets/CM-T1.3.md) - Monitor file changes
4. [CM-T1.4: Basic Code Snippet Extraction](./tickets/CM-T1.4.md) - Extract relevant code portions
5. [CM-T1.5: Send Code to Companion App](./tickets/CM-T1.5.md) - Transmit data to backend
6. [CM-T1.6: Plugin Activation & Deactivation](./tickets/CM-T1.6.md) - Manage extension lifecycle

## Success Criteria
- Extension can be installed and activated in VS Code
- File changes are detected and monitored
- Code snippets are extracted and transmitted to companion app
- Communication channel is stable and responsive 