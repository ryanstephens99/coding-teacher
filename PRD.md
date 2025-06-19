Product Requirements Document: CodeMentor AI
1. Introduction
1.1 Project Title
CodeMentor AI: The Intelligent Convention Teacher

1.2 Overview
CodeMentor AI is an innovative desktop companion application designed to integrate directly with the Cursor IDE as a plugin. Its primary purpose is to act as a personalized, non-invasive coding teacher, providing real-time feedback on code convention adherence. Unlike traditional linters that merely flag errors, CodeMentor AI will explain why specific conventions are recommended, fostering deeper understanding and improving coding practices.

1.3 Goals
Enhance Code Quality: Help developers write cleaner, more maintainable, and idiomatic code by adhering to established conventions.

Accelerate Learning: Provide contextual, on-demand explanations for conventions, turning passive error correction into an active learning experience.

Improve Developer Productivity: Offer immediate, actionable feedback and potential quick-fixes, reducing time spent on manual style reviews or debugging convention-related issues.

Foster Best Practices: Instill a strong understanding of coding ideals and industry best practices in users.

1.4 Target Audience
Beginner to Intermediate Developers: Those still learning established coding conventions and seeking guidance.

Developers Switching Languages/Frameworks: Individuals needing to quickly adapt to new convention sets.

Teams Aiming for Code Consistency: Groups wanting to enforce a unified style guide across their codebase.

Individual Learners: Anyone passionate about improving their code quality and understanding the "why" behind coding standards.

2. User Stories
2.1 Core Interaction User Stories
As a developer using Cursor IDE, I want CodeMentor AI to highlight code that deviates from established conventions, so that I'm immediately aware of areas needing attention.

As a developer new to a specific language/framework, I want to hover over highlighted code, so that I can quickly see a brief explanation of the convention issue and a suggested correction without interrupting my flow.

As a developer seeking deeper understanding, I want to click on highlighted code, so that a detailed side panel appears with a full explanation, example, and reasoning behind the convention.

As a learner encountering a convention, I want to ask follow-up questions within the side panel, so that I can clarify my understanding and explore nuances of the rule.

As a developer wanting to quickly fix an issue, I want to see a "Fix" button in the side panel for suggested changes, so that I can automatically apply the recommended convention.

2.2 Learning & Customization User Stories
As a developer wanting to understand the "why", I want the side panel to explain the reasoning and benefits of each convention, so that I can grasp the importance beyond just knowing the rule.

As a developer adopting new conventions, I want CodeMentor AI to maintain a formal but encouraging tone, so that I feel supported in improving my coding style rather than being simply corrected.

As a developer interested in best practices, I want the side panel to provide links to external documentation or style guides, so that I can perform further research if desired.

3. Features
3.1 Code Analysis & Convention Detection
Real-time Code Monitoring: The plugin will continuously analyze the active code file in the Cursor IDE as the user types or saves.

Convention Rule Sets:

Pre-defined Rules: Initial support for common coding conventions (e.g., variable naming, function structure, comment styles, indentation) for popular languages. Specific languages and style guides will be prioritized during development.

Contextual Analysis: Ability to understand the programming language and potentially the framework in use to apply relevant conventions.

Accuracy & Performance: The analysis must be fast enough to provide real-time feedback without noticeably slowing down the IDE.

3.2 In-IDE Visual Feedback
Contextual Highlighting:

When a convention violation is detected, the relevant code segment will be highlighted directly in the editor.

Highlighting will be non-intrusive, potentially using a subtle background color or underline that distinguishes it from syntax errors.

Hover Tooltip:

On hover over highlighted code, a small, concise tooltip will appear.

This tooltip will include the problem description (e.g., "Non-standard variable naming") and a brief suggested correction (e.g., "Consider myVariable instead of my_variable").

3.3 Interactive Learning Panel
Side Panel Integration: A dedicated side panel will open within Cursor when highlighted code is clicked.

Detailed Explanation Display: The panel will provide:

Clear Problem Statement: A formal description of the convention violation.

Suggested Code Correction: The ideal way the code should look, with a clear example.

Comprehensive Reasoning: A detailed explanation of why the convention is best practice, emphasizing readability, maintainability, performance, etc. This will be formal but encouraging in tone.

Code Examples: Illustrative snippets showing correct and possibly incorrect usage.

External Resources (Optional): Links to official style guides, documentation, or relevant articles for deeper dives.

Q&A Interface:

An input field within the side panel where users can type questions related to the highlighted convention or general coding best practices.

An AI-powered response mechanism that provides contextual, accurate answers in the same formal but encouraging tone, reinforcing the teaching aspect.

The AI will be designed to "stand its ground" on coding ideals, providing explanations rooted in best practices rather than being easily persuaded otherwise.

Issue Navigation: If multiple issues exist in a file, the panel could allow navigation between them.

3.4 Correction & Improvement Tools
Auto-Fix Button: For applicable convention violations, a "Fix" button will be present in the side panel, allowing the user to automatically apply the suggested correction to their code with a single click.

3.5 Technical Foundation (High-Level)
Cursor IDE Plugin: Developed using Cursor's (VS Code's) extension API.

Desktop Companion App: A background service running on the user's machine.

4. User Experience (UX)
4.1 Overall User Journey
The user journey is designed to be continuous and supportive, moving from passive awareness to active learning and correction:

Passive Awareness: Developer codes in Cursor, and CodeMentor AI silently monitors.

Immediate Notification: Deviation from convention is detected, and the relevant code is highlighted in real-time.

Quick Insight: Developer hovers over the highlight, and a concise tooltip provides a brief problem description and suggested correction.

Deep Dive & Interaction: Developer clicks the highlight, opening the interactive side panel for detailed explanations and the ability to ask follow-up questions.

Correction: Developer can choose to auto-fix the issue via the side panel or manually apply the learned correction.

4.2 Visual Design & Interaction Principles
Non-Intrusive Highlighting:

Highlighting will be subtle but distinct, ensuring it doesn't obscure code readability or conflict with Cursor's native highlighting (e.g., syntax errors, search results). A soft background color or a distinct underline will be used.

The highlight will only appear when a convention violation is detected, and disappear upon correction.

Contextual Tooltips:

Tooltips will appear quickly on hover, be concise, and disappear naturally when the mouse moves away.

They will use clear, straightforward language.

Integrated Side Panel:

The side panel will seamlessly integrate into Cursor's existing UI layout (e.g., appearing as a tab or separate panel alongside other IDE tools like "Problems," "Output," or "Chat").

It will be visually clean, well-organized, and easy to read.

Clear Information Hierarchy:

Within the side panel, information (problem, suggestion, reasoning, examples) will be clearly separated and easy to scan.

Important elements (like the "Fix" button) will be visually prominent.

Intuitive Q&A Interface:

The Q&A input field will be clearly labeled and easy to use.

AI responses will be presented in a readable format, potentially using markdown for code blocks or emphasis.

Consistency: UI elements, terminology, and interaction patterns will be consistent throughout the plugin.

4.3 Tone and Language
Formal but Encouraging: The language used in explanations and Q&A responses will be professional, clear, and authoritative on best practices, while maintaining an encouraging and supportive tone for the learner.

Educational Focus: Emphasis on explaining the "why" and "best practice" behind conventions, rather than simply stating "wrong" or "correct."

Unwavering on Ideals: The AI's suggestions and explanations regarding coding conventions will be firm and consistent, upholding established coding ideals without being easily "talked out of" a recommendation by user questions. The goal is to teach and guide towards best practices.

5. Technical Considerations
5.1 Overall Architecture
CodeMentor AI will employ a two-component architecture to leverage the best of both worlds: deep IDE integration and powerful, scalable analysis capabilities.

Cursor IDE Plugin: Handles real-time code capture, visual feedback (highlighting, tooltips), and rendering of the interactive side panel within the IDE.

Desktop Companion Application/Service: Runs in the background on the user's machine. This service will be responsible for the heavy lifting of code analysis, convention rule enforcement, and processing AI-driven Q&A.

5.2 Cursor IDE Plugin Responsibilities
The Cursor plugin (built using the VS Code Extension API, which Cursor extends) will primarily focus on interaction and presentation:

Code Document Access: Listen to changes in the active code document in real-time.

Code Snippet Extraction: Extract relevant code sections that need analysis.

Communication with Companion App: Send code snippets to the desktop companion app for analysis and receive analysis results/suggestions.

Text Decorations/Highlighting: Apply custom highlighting to code segments based on feedback from the companion app.

Hover Provider: Implement hover providers to display concise tooltips on highlighted code.

Webview Panel Management: Manage the lifecycle and content of the interactive side panel (a "webview" in VS Code terminology).

User Input Capture: Send user questions from the Q&A interface to the companion app.

"Fix" Command Execution: Apply automated code changes received from the companion app.

5.3 Desktop Companion Application/Service Responsibilities
This background service will handle the intelligence of CodeMentor AI:

Convention Rule Engine:

Implement robust parsing and abstract syntax tree (AST) analysis for supported programming languages.

Store and apply the defined convention rule sets.

Perform static code analysis to identify violations.

Contextual Reasoning Generator:

Based on detected violations, generate detailed explanations, reasoning ("why it's best convention"), and example code snippets.

AI/LLM Integration for Q&A:

Integrate with a Large Language Model (LLM) to power the interactive Q&A functionality. Initial implementation will likely utilize a cloud-based LLM API (e.g., Google Gemini, OpenAI GPT, Anthropic).

Prompt engineering will be critical to ensure the LLM maintains the formal, encouraging, and "stands its ground" tone.

Inter-Process Communication (IPC): Establish a reliable and secure communication channel with the Cursor IDE plugin (e.g., via a local HTTP server or WebSockets).

Auto-Fix Logic: Generate the precise code edits required for the "Fix" button.

5.4 Data Flow (High-Level)
Code Change: User types/saves code in Cursor.

Plugin Captures: Cursor plugin captures the relevant code and sends it via IPC to the Desktop Companion App.

App Analyzes: Companion App performs convention analysis.

App Responds: Companion App sends back detected issues, suggested highlights, and metadata for tooltips/side panel.

Plugin Renders: Plugin applies highlights and prepares tooltip data.

User Interacts (Click): User clicks highlight; Plugin sends request to Companion App for detailed explanation.

App Generates Explanation: Companion App retrieves/generates detailed explanation and potentially uses LLM for Q&A.

Plugin Renders Panel: Plugin renders the side panel with explanations and Q&A.

5.5 Key Technologies (Preliminary)
Frontend (Plugin): TypeScript, VS Code Extension API (JavaScript/TypeScript).

Backend (Companion App): Python with FastAPI.

AI/LLM: Choice of specific LLM provider/model (e.g., Google Gemini, OpenAI GPT).

IPC: Local WebSockets, HTTP REST API.

6. Success Metrics
These metrics will help us assess CodeMentor AI's impact on users' coding practices and learning.

6.1 User Engagement & Adoption
Plugin Downloads/Installations: Track the number of unique installations of the CodeMentor AI plugin.

Active Users (DAU/WAU/MAU): Monitor the number of daily, weekly, and monthly active users.

Session Duration/Frequency: How long and how often users are interacting with the side panel.

Feature Usage:

Hover-Tooltip Interactions: Number of times users hover over highlighted code.

Side Panel Opens: Number of times users click on highlighted code to open the side panel.

Q&A Usage: Frequency of questions asked within the side panel.

"Fix" Button Usage: Number of times the auto-fix button is utilized.

6.2 Learning & Code Quality Impact
Convention Adherence Rate (Over Time): Measure the rate at which suggested fixes are adopted or highlighted issues are resolved (manually or via auto-fix).

User Satisfaction (CSAT/NPS): Gather feedback on overall user satisfaction through in-app surveys.

6.3 Performance & Reliability
Analysis Latency: Measure the time taken for the companion app to analyze code and return results.

Plugin Responsiveness: Monitor for any reported slowdowns or freezing of the Cursor IDE.

Bug/Crash Reports: Track the number and severity of reported bugs or crashes.

7. Out of Scope for Initial Release
To ensure a focused and timely initial release, the following features and functionalities are explicitly considered out of scope for CodeMentor AI v1.0. These may be considered for future iterations based on user feedback and strategic priorities.

Customizable Rule Sets: The ability for users to define their own custom convention rules or import external, non-standard style guides.

Multi-IDE Support: Initial development will strictly focus on the Cursor IDE plugin.

Advanced Refactoring Tools: Beyond simple auto-fixes for convention violations, complex code refactoring suggestions or tools (e.g., extracting methods, changing function signatures across files) are out of scope.

Full Project-Wide Analysis: Initial analysis will focus primarily on the currently active file or selected code blocks. Comprehensive, real-time project-wide analysis that spans multiple files and directories is out of scope.

Offline AI/LLM: The initial release's Q&A functionality will rely on a cloud-based LLM API, requiring an internet connection.

Historical Performance Tracking/Dashboards: No in-app dashboards or user-facing historical reporting on a user's convention adherence over time will be included.

Team/Collaboration Features: Features enabling team-wide style guide enforcement, sharing custom rules, or collaborative learning are not part of the initial scope.

Monetization/Licensing: The initial release will not include any monetization or complex licensing mechanisms.

8. Future Considerations / Roadmap
This section outlines potential features and enhancements for CodeMentor AI in future iterations, to be prioritized based on user feedback, market demand, and strategic goals.

8.1 Enhanced Code Analysis & Scope
Full Project-Wide Analysis: Ability to analyze an entire project or selected directories, providing a holistic view of convention adherence.

Advanced Refactoring Suggestions: Suggestions for more complex code improvements (e.g., "extract method," "rename symbol across multiple files").

Customizable Rule Sets: Allow users to define and import their own custom convention rules.

8.2 Learning & Interaction Improvements
Offline LLM Support: Enable the Q&A functionality to work entirely offline.

Gamification/Progress Tracking: Features to track a user's progress in adopting conventions over time.

Interactive Tutorials: Short, guided tutorials explaining complex conventions.

Multimedia Explanations: Incorporate diagrams, animations, or short video snippets within explanations.

8.3 Platform & Integration Expansion
Multi-IDE Support: Extend plugin development to other popular desktop IDEs (e.g., VS Code, IntelliJ IDEA) and potentially web-based IDEs.

Version Control Integration: Provide feedback on convention violations directly within pull request/code review interfaces.

8.4 Community & Collaboration Features
Team Style Guides: Features to share and enforce consistent style guides across development teams.

Collaborative Learning: Ability to share insights or questions with teammates directly through the app.