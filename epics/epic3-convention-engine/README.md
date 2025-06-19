# Epic 3: Convention Rule Engine & Code Analysis

## Overview
Build a sophisticated rule engine that can analyze code patterns and detect convention violations using AST parsing.

## Goal
Create a flexible, extensible system for defining and executing coding convention rules that can analyze code structure, detect violations, and suggest improvements.

## Key Technologies
- Python AST parsing
- Rule definition DSL
- Pattern matching
- Static analysis
- Configurable rule system

## Dependencies
- Requires Epic 2 (companion app) for integration
- Built on research of modern AST parsing and analysis tools

## Estimated Effort
3-4 weeks

## Architecture Decisions
Based on research into AST parsing and static analysis best practices:
- Use Python's built-in AST module for reliable parsing
- Implement visitor pattern for efficient tree traversal
- Create declarative rule definition language
- Support both built-in and custom rules
- Focus on extensibility and performance

## Tickets
1. [CM-T3.1: AST Parser & Tree Walker](./tickets/CM-T3.1.md) - Core AST parsing infrastructure
2. [CM-T3.2: Rule Definition System](./tickets/CM-T3.2.md) - Flexible rule configuration and definition
3. [CM-T3.3: Pattern Matching Engine](./tickets/CM-T3.3.md) - Advanced pattern detection for code analysis
4. [CM-T3.4: Built-in Convention Rules](./tickets/CM-T3.4.md) - Standard coding convention rules
5. [CM-T3.5: Violation Detection & Reporting](./tickets/CM-T3.5.md) - Results processing and reporting
6. [CM-T3.6: Performance Optimization](./tickets/CM-T3.6.md) - Caching and performance improvements

## Success Criteria
- AST parsing works reliably for multiple languages
- Rule engine can detect complex code patterns
- Performance is acceptable for real-time analysis
- Rules are easily configurable and extensible
- Violation reports are clear and actionable 