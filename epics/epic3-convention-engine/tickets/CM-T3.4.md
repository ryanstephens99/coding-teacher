# CM-T3.4: Implement Convention Rule 2 (Indentation)

## Summary
Implement Python indentation convention rules based on PEP 8, including 4-space indentation validation, mixed indentation detection, and line length limits.

## Acceptance Criteria
- [ ] 4-space indentation validation for Python code
- [ ] Mixed indentation detection (spaces vs tabs)
- [ ] Consistent indentation depth checking
- [ ] Line length validation (79 characters maximum)
- [ ] Context-aware indentation rules for different code structures
- [ ] Performance optimization for large files

## Implementation Details

This ticket implements the second core coding convention rule, focusing on Python indentation and formatting standards as specified in PEP 8. The rule will analyze source code text to identify formatting violations.

### Key Components
1. **Indentation Analyzer** - Line-by-line indentation analysis
2. **Mixed Indentation Detector** - Detect tabs vs spaces inconsistencies
3. **Line Length Validator** - Check maximum line length limits
4. **Indentation Stack Tracker** - Track indentation context and nesting
5. **Formatting Fix Suggester** - Generate indentation corrections

### Indentation Rules

**4-Space Indentation Standard:**
- Each indentation level must be exactly 4 spaces
- No tabs allowed for indentation
- Consistent indentation depth throughout file
- Proper indentation for nested structures (functions, classes, conditionals)

**Mixed Indentation Detection:**
- Scan entire file for tab characters in indentation
- Detect inconsistent spacing (2-space, 8-space, etc.)
- Flag lines that mix tabs and spaces
- Report inconsistent indentation within same block

**Line Length Validation:**
- Maximum 79 characters per line (PEP 8 standard)
- Exclude comment lines with URLs or long strings
- Provide suggestions for line breaking
- Handle special cases (imports, string literals)

### Context-Aware Analysis

**Code Structure Recognition:**
- Function and method definitions
- Class definitions and methods
- Conditional statements (if/elif/else)
- Loop structures (for/while)
- Exception handling (try/except/finally)
- Context managers (with statements)

**Indentation Context Tracking:**
- Maintain indentation stack for nested structures
- Validate proper indentation increases/decreases
- Detect hanging indents and continuation lines
- Handle multi-line expressions and statements

**Special Cases:**
- Multi-line function arguments
- List/dictionary comprehensions
- Long string literals and comments
- Import statements and from imports
- Decorator applications

### Violation Detection

**Indentation Violations:**
- Incorrect indentation depth (not multiple of 4)
- Mixed tabs and spaces
- Inconsistent indentation within block
- Missing indentation for nested code
- Excessive indentation (more than necessary)

**Line Length Violations:**
- Lines exceeding 79 character limit
- Provide context about why line is too long
- Suggest appropriate line breaking strategies
- Handle edge cases appropriately

### Fix Suggestions

**Indentation Fixes:**
- Convert tabs to 4 spaces
- Adjust indentation to proper 4-space increments
- Fix inconsistent indentation within blocks
- Suggest proper indentation for nested structures

**Line Length Fixes:**
- Suggest natural breaking points (after commas, operators)
- Recommend parentheses for line continuation
- Propose variable extraction for complex expressions
- Handle import statement formatting

## Technical Notes
- Analyzes source code text line-by-line for indentation
- Uses regex patterns for efficient whitespace detection
- Implements stack-based tracking for indentation context
- Provides detailed fix suggestions with examples
- Optimized for performance with large files

## Dependencies
- CM-T3.1 for language and convention selection
- CM-T3.2 for AST parsing infrastructure
- CM-T3.3 for base rule class and violation models
- Python string processing utilities
- Regular expression engine

## Testing
- Validate correct 4-space indentation passes without violations
- Detect all types of indentation violations
- Mixed indentation detection works correctly
- Line length validation catches violations accurately
- Fix suggestions are helpful and correct

## Estimated Hours
6-8 hours 