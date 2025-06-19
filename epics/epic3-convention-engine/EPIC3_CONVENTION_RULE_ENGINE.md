# Epic 3: Convention Rule Engine & Basic Analysis

Core logic for identifying code convention violations using Abstract Syntax Tree (AST) parsing and rule-based analysis for multiple programming languages.

## Completed Tasks

- [ ] None yet - starting fresh implementation

## In Progress Tasks

- [ ] CM-T3.1: Choose Initial Language & Conventions
- [ ] CM-T3.2: Code Parsing & AST Setup
- [ ] CM-T3.3: Implement Convention Rule 1 (Variable Naming)
- [ ] CM-T3.4: Implement Convention Rule 2 (Indentation)
- [ ] CM-T3.5: Integrate Rule Engine with IPC Input
- [ ] CM-T3.6: Basic Error Handling in Analysis

## Future Tasks

- [ ] Multi-language support expansion
- [ ] Performance optimization for large files
- [ ] Custom rule configuration
- [ ] Rule severity customization
- [ ] Advanced semantic analysis

## Implementation Plan

### Architecture Overview
The convention rule engine will use language-specific AST parsers to analyze code structure and apply configurable rules. We'll start with Python (using the built-in `ast` module) and JavaScript/TypeScript (using tree-sitter or esprima), implementing common conventions like naming, indentation, and code structure rules.

### Technical Stack
- **Python**: Built-in `ast` module for Python code analysis
- **JavaScript/TypeScript**: tree-sitter-javascript for robust parsing
- **Rule Engine**: Plugin-based architecture for extensible rules
- **Performance**: Async processing with caching for large files
- **Configuration**: YAML/JSON-based rule configuration

## Detailed Ticket Implementation

### CM-T3.1: Choose Initial Language & Conventions

**Technical Requirements:**
- Language selection based on popularity and parsing capabilities
- Convention research from established style guides
- Rule prioritization based on educational value
- Performance considerations for real-time analysis

**Implementation Steps:**
1. **Language Selection Analysis:**
   - **Python**: Excellent AST support, PEP 8 conventions, beginner-friendly
   - **JavaScript**: High usage, multiple style guides (ESLint, Standard)
   - **TypeScript**: Growing adoption, strict typing conventions
   - **Decision**: Start with Python for robust AST support

2. **Python Convention Selection (PEP 8 Based):**
   - Variable naming: snake_case for variables/functions
   - Class naming: PascalCase for classes
   - Constant naming: SCREAMING_SNAKE_CASE for constants
   - Indentation: 4 spaces per level
   - Line length: 79 characters maximum
   - Import organization: stdlib, third-party, local

3. **Rule Priority Matrix:**
   - HIGH: naming_conventions, indentation_4_spaces
   - MEDIUM: line_length_79, blank_lines_functions
   - LOW: import_organization, docstring_functions

**Files to Create:**
- `app/analysis/rules/python_rules.py` - Python convention definitions
- `app/analysis/config/rule_priorities.yaml` - Rule priority configuration
- `docs/supported_conventions.md` - Documentation of supported rules

### CM-T3.2: Code Parsing & AST Setup

**Technical Requirements:**
- Robust AST parsing with error recovery
- Language detection and parser selection
- Performance optimization for real-time analysis
- Memory-efficient tree traversal
- Support for incomplete/invalid code

**Implementation Steps:**
1. Install parsing dependencies: `tree-sitter`, `tree-sitter-python`, `tree-sitter-javascript`
2. Create abstract parser interface with ParseResult and SourceLocation models
3. Implement Python AST parser with syntax error recovery
4. Create parser factory for language detection and parser selection
5. Add performance monitoring and memory usage tracking

**Files to Create:**
- `app/analysis/parsers/base_parser.py` - Abstract parser interface
- `app/analysis/parsers/python_parser.py` - Python AST parser implementation
- `app/analysis/parsers/parser_factory.py` - Parser selection and management
- `app/analysis/models/ast_models.py` - AST-related data models

### CM-T3.3: Implement Convention Rule 1 (Variable Naming)

**Technical Requirements:**
- Snake_case validation for Python variables
- Class name PascalCase validation
- Constant SCREAMING_SNAKE_CASE validation
- Context-aware rule application
- Detailed violation descriptions

**Implementation Steps:**
1. Create base rule class with RuleViolation model
2. Implement Python variable naming rule with regex patterns
3. Add context-aware analysis for variables, functions, classes
4. Create suggested fix generation for naming violations
5. Add comprehensive explanations for educational value

**Files to Create:**
- `app/analysis/rules/base_rule.py` - Abstract rule interface
- `app/analysis/rules/python/naming_rules.py` - Python naming convention rules
- `app/analysis/models/violation_models.py` - Rule violation data models

### CM-T3.4: Implement Convention Rule 2 (Indentation)

**Technical Requirements:**
- 4-space indentation validation for Python
- Mixed indentation detection (spaces vs tabs)
- Consistent indentation depth checking
- Context-aware indentation rules
- Performance optimization for large files

**Implementation Steps:**
1. Implement indentation analysis with line-by-line processing
2. Add mixed tab/space detection across entire file
3. Create line length validation rule (79 characters)
4. Add indentation stack tracking for context awareness
5. Generate specific fix suggestions for indentation issues

**Files to Create:**
- `app/analysis/rules/python/indentation_rules.py` - Python indentation rules
- `app/analysis/rules/python/line_length_rules.py` - Line length validation
- `app/analysis/utils/indentation_analyzer.py` - Indentation analysis utilities

### CM-T3.5: Integrate Rule Engine with IPC Input

**Technical Requirements:**
- Rule engine orchestration and execution
- Integration with FastAPI endpoints
- Async rule processing for performance
- Result aggregation and formatting
- Error handling and fallback mechanisms

**Implementation Steps:**
1. Create rule engine orchestrator with async rule execution
2. Update FastAPI code processor to use rule engine
3. Add violation-to-ConventionIssue conversion
4. Implement concurrent rule processing with error isolation
5. Add comprehensive metadata and performance tracking

**Files to Create:**
- `app/analysis/engine/rule_engine.py` - Main rule engine orchestrator
- `app/analysis/engine/__init__.py` - Engine package initialization
- `app/services/code_processor.py` - Updated with rule engine integration

### CM-T3.6: Basic Error Handling in Analysis

**Technical Requirements:**
- Graceful handling of malformed code
- Partial analysis capability for syntax errors
- Performance monitoring and timeouts
- Detailed error reporting and logging
- Recovery mechanisms for failed rules

**Implementation Steps:**
1. Create custom exception classes for analysis errors
2. Implement timeout protection with async context managers
3. Add safe rule execution with error isolation
4. Create performance monitoring with memory tracking
5. Add comprehensive error logging and recovery mechanisms

**Files to Create:**
- `app/analysis/engine/error_handler.py` - Error handling utilities
- `app/analysis/engine/performance_monitor.py` - Performance monitoring
- `app/analysis/exceptions.py` - Custom exception classes

## Relevant Files

- `app/analysis/rules/base_rule.py` - Abstract rule interface ✅
- `app/analysis/rules/python/naming_rules.py` - Python naming conventions ✅
- `app/analysis/rules/python/indentation_rules.py` - Python indentation rules ✅
- `app/analysis/parsers/python_parser.py` - Python AST parser ✅
- `app/analysis/parsers/parser_factory.py` - Parser management ✅
- `app/analysis/engine/rule_engine.py` - Rule orchestration engine ✅
- `app/analysis/engine/error_handler.py` - Error handling system ✅
- `app/analysis/engine/performance_monitor.py` - Performance monitoring ✅
- `app/services/code_processor.py` - Updated with rule engine ✅
- `app/analysis/config/rule_priorities.yaml` - Rule configuration ✅

## Technical Considerations

### Performance Optimization
- Async rule execution for concurrent processing
- AST caching for repeated analysis of same code
- Incremental analysis for large files
- Memory usage monitoring and limits

### Extensibility
- Plugin-based rule architecture
- Language-specific rule packages
- Configurable rule severity levels
- Custom rule development framework

### Error Recovery
- Partial analysis for syntax errors
- Graceful rule failure handling
- Timeout protection for long-running analysis
- Detailed error reporting and logging

### Testing Strategy
- Unit tests for individual rules
- Integration tests with various code samples
- Performance benchmarks for large files
- Error condition testing 