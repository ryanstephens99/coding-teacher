# CodeMentor AI - Master Task Overview

Comprehensive task breakdown for the CodeMentor AI intelligent coding convention teacher project.

## Project Status Dashboard

### Epic Progress Overview
- **Epic 1**: Core IDE Plugin & Real-time Monitoring - 🔄 **In Progress** (0/6 tickets)
- **Epic 2**: Desktop Companion App - Core Service & IPC Server - 🔄 **In Progress** (0/5 tickets)  
- **Epic 3**: Convention Rule Engine & Basic Analysis - 🔄 **In Progress** (0/6 tickets)
- **Epic 4**: In-IDE Visual Feedback & Tooltips - 🔄 **In Progress** (0/4 tickets)
- **Epic 5**: AI/LLM Integration for Educational Explanations - 🔄 **In Progress** (0/5 tickets)

**Total Progress**: 0/26 tickets completed (0%)

## Epic Breakdown

### Epic 1: Core IDE Plugin & Real-time Monitoring
**Goal**: Enable CodeMentor AI to listen to code changes in Cursor and communicate with the backend service.

**Key Technologies**: TypeScript, VS Code Extension API, WebSocket/IPC, Node.js

**Tickets**:
- [ ] CM-T1.1: Plugin Project Setup (TypeScript)
- [ ] CM-T1.2: Establish IPC Client in Plugin  
- [ ] CM-T1.3: Code Document Change Listener
- [ ] CM-T1.4: Basic Code Snippet Extraction
- [ ] CM-T1.5: Send Code to Companion App (Initial)
- [ ] CM-T1.6: Plugin Activation & Deactivation

**Dependencies**: None (foundational)
**Estimated Effort**: 2-3 weeks

### Epic 2: Desktop Companion App - Core Service & IPC Server
**Goal**: Create the FastAPI backend service that communicates with the plugin and hosts analysis logic.

**Key Technologies**: Python, FastAPI, WebSocket/IPC, Pydantic, Uvicorn

**Tickets**:
- [ ] CM-T2.1: FastAPI Project Setup (Python)
- [ ] CM-T2.2: Establish IPC Server in FastAPI
- [ ] CM-T2.3: Receive & Log Code from Plugin
- [ ] CM-T2.4: Basic Service Health Check
- [ ] CM-T2.5: Companion App Packaging (Basic)

**Dependencies**: Epic 1 (for IPC communication)
**Estimated Effort**: 2-3 weeks

### Epic 3: Convention Rule Engine & Basic Analysis
**Goal**: Implement core logic for identifying code convention violations using AST parsing.

**Key Technologies**: Python AST, tree-sitter, regex patterns, async processing

**Tickets**:
- [ ] CM-T3.1: Choose Initial Language & Conventions
- [ ] CM-T3.2: Code Parsing & AST Setup
- [ ] CM-T3.3: Implement Convention Rule 1 (Variable Naming)
- [ ] CM-T3.4: Implement Convention Rule 2 (Indentation)
- [ ] CM-T3.5: Integrate Rule Engine with IPC Input
- [ ] CM-T3.6: Basic Error Handling in Analysis

**Dependencies**: Epic 2 (for integration)
**Estimated Effort**: 3-4 weeks

### Epic 4: In-IDE Visual Feedback & Tooltips
**Goal**: Display convention violations directly within Cursor IDE through highlighting and tooltips.

**Key Technologies**: VS Code Extension API, TextEditorDecorationType, HoverProvider, Markdown

**Tickets**:
- [ ] CM-T4.1: Receive & Process Analysis Results in Plugin
- [ ] CM-T4.2: Implement Contextual Highlighting
- [ ] CM-T4.3: Implement Hover Provider for Tooltips
- [ ] CM-T4.4: Clear Highlights on Document Close/No Issues

**Dependencies**: Epic 1 (plugin foundation), Epic 3 (analysis results)
**Estimated Effort**: 2-3 weeks

### Epic 5: AI/LLM Integration for Educational Explanations
**Goal**: Integrate with OpenAI GPT API to provide context-aware educational explanations.

**Key Technologies**: OpenAI API, GPT-4, prompt engineering, caching, rate limiting

**Tickets**:
- [ ] CM-T5.1: OpenAI API Integration Setup
- [ ] CM-T5.2: Context-Aware Prompt Engineering
- [ ] CM-T5.3: Educational Content Generation
- [ ] CM-T5.4: Caching & Rate Limiting
- [ ] CM-T5.5: Fallback Mechanisms & Error Handling

**Dependencies**: Epic 2 (companion app), Epic 3 (rule violations)
**Estimated Effort**: 3-4 weeks

## Development Phases

### Phase 1: Foundation (Weeks 1-4)
**Focus**: Core infrastructure and basic communication
- Epic 1: Complete plugin setup and IPC client
- Epic 2: Complete FastAPI service and IPC server
- **Milestone**: Plugin can send code to companion app and receive responses

### Phase 2: Analysis Engine (Weeks 5-8)
**Focus**: Convention detection and rule processing
- Epic 3: Complete rule engine with Python conventions
- Epic 4: Basic visual feedback implementation
- **Milestone**: Real-time convention violation detection and highlighting

### Phase 3: Enhanced Experience (Weeks 9-12)
**Focus**: AI integration and polished user experience
- Epic 4: Complete visual feedback with rich tooltips
- Epic 5: AI-powered educational explanations
- **Milestone**: Full educational experience with AI-generated content

## Critical Path Analysis

**Longest Path**: Epic 1 → Epic 2 → Epic 3 → Epic 4 → Epic 5
**Critical Dependencies**:
1. IPC communication (Epic 1 ↔ Epic 2)
2. Analysis results (Epic 3 → Epic 4)
3. Rule violations (Epic 3 → Epic 5)

## Risk Assessment

### High Risk
- **IPC Communication Complexity**: WebSocket/named pipe implementation across plugin and desktop app
- **VS Code API Limitations**: Potential restrictions in extension capabilities
- **OpenAI API Costs**: Usage costs could escalate during development/testing

### Medium Risk  
- **AST Parsing Performance**: Large file analysis might be slow
- **Cross-platform Compatibility**: Desktop app deployment across OS
- **Rate Limiting**: OpenAI API quotas and throttling

### Low Risk
- **Python Convention Rules**: Well-documented PEP 8 standards
- **FastAPI Implementation**: Mature framework with good documentation
- **TypeScript Plugin Development**: Established VS Code extension patterns

## Resource Requirements

### Development Environment
- **Languages**: TypeScript, Python 3.9+
- **Frameworks**: VS Code Extension API, FastAPI, React (future)
- **Tools**: Node.js, npm/yarn, pip, pytest, jest
- **Services**: OpenAI API account, Redis (optional caching)

### External Dependencies
- **OpenAI API**: GPT-4 access for educational content
- **VS Code**: Extension development and testing
- **Python Libraries**: FastAPI, Pydantic, tree-sitter, openai
- **Node Libraries**: vscode, ws, typescript

## Success Metrics

### Technical Metrics
- **Response Time**: < 500ms for convention analysis
- **Accuracy**: > 95% for convention detection
- **Performance**: Handle files up to 10,000 lines
- **Reliability**: < 1% error rate in analysis

### User Experience Metrics
- **Educational Value**: User comprehension improvement
- **Non-intrusiveness**: Minimal disruption to coding flow
- **Adoption**: Daily active usage by developers
- **Satisfaction**: Positive feedback on explanations

## Next Steps

1. **Immediate (This Week)**:
   - Set up development environment
   - Initialize Epic 1 tickets
   - Create project repository structure

2. **Short Term (Next 2 Weeks)**:
   - Complete CM-T1.1 and CM-T1.2
   - Begin Epic 2 setup in parallel
   - Establish basic IPC communication

3. **Medium Term (Next Month)**:
   - Complete Phase 1 milestone
   - Begin rule engine development
   - Test end-to-end communication flow 