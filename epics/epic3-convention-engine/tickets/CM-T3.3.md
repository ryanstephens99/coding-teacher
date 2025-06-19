# CM-T3.3: Implement Convention Rule 1 (Variable Naming)

## Summary
Implement Python variable naming convention rules based on PEP 8, including snake_case validation for variables/functions, PascalCase for classes, and SCREAMING_SNAKE_CASE for constants.

## Acceptance Criteria
- [ ] Snake_case validation for Python variables and functions
- [ ] PascalCase validation for class names
- [ ] SCREAMING_SNAKE_CASE validation for constants
- [ ] Context-aware rule application (distinguish variables from imports)
- [ ] Detailed violation descriptions with suggested fixes
- [ ] Performance optimization for real-time analysis

## Implementation Details

This ticket implements the first concrete coding convention rule, focusing on Python naming conventions as specified in PEP 8. The rule will analyze AST nodes to identify naming violations and provide educational feedback.

### Key Components
1. **Base Rule Class** - Abstract interface for all convention rules
2. **Naming Rule Implementation** - Python-specific naming convention logic
3. **Rule Violation Model** - Structured violation reporting
4. **Context Analyzer** - Determine naming context (variable, function, class, constant)
5. **Fix Suggester** - Generate suggested naming corrections

### Naming Convention Rules

**Snake_case for Variables and Functions:**
- Pattern: `^[a-z_][a-z0-9_]*$`
- Valid: `user_name`, `calculate_total`, `_private_var`
- Invalid: `userName`, `calculateTotal`, `UserName`

**PascalCase for Classes:**
- Pattern: `^[A-Z][a-zA-Z0-9]*$`
- Valid: `UserAccount`, `HttpClient`, `DatabaseConnection`
- Invalid: `userAccount`, `httpClient`, `database_connection`

**SCREAMING_SNAKE_CASE for Constants:**
- Pattern: `^[A-Z][A-Z0-9_]*$`
- Valid: `MAX_SIZE`, `API_KEY`, `DEFAULT_TIMEOUT`
- Invalid: `max_size`, `Api_Key`, `defaultTimeout`

### Context-Aware Analysis

**Variable Context Detection:**
- Function parameters and local variables
- Class instance variables
- Module-level variables
- Loop variables and comprehensions

**Function Context Detection:**
- Function definitions (`def` statements)
- Method definitions within classes
- Lambda functions and closures
- Async function definitions

**Class Context Detection:**
- Class definitions (`class` statements)
- Nested class definitions
- Abstract base classes

**Constant Context Detection:**
- Module-level assignments with ALL_CAPS names
- Class-level variables that don't change
- Variables assigned literal values (strings, numbers)

### Violation Reporting

**Violation Structure:**
- Rule ID and name
- Violation location (file, line, column)
- Current name and suggested fix
- Educational explanation
- Severity level (error, warning, info)

**Educational Content:**
- Explanation of why the naming convention exists
- Examples of good and bad naming
- Links to PEP 8 documentation
- Context about readability and maintainability

## Technical Notes
- Uses Python AST module for reliable node analysis
- Implements regex patterns for efficient name validation
- Provides context-aware analysis to avoid false positives
- Generates actionable fix suggestions for violations
- Optimized for real-time analysis with minimal overhead

## Dependencies
- CM-T3.1 for language and convention selection
- CM-T3.2 for AST parsing infrastructure
- Python built-in `ast` module
- Regular expression engine
- Rule violation data models

## Testing
- Validate correct naming patterns pass without violations
- Detect all specified naming convention violations
- Context analysis correctly identifies variable types
- Suggested fixes are accurate and helpful
- Performance is acceptable for real-time analysis

## Estimated Hours
6-8 hours 