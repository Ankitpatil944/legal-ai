# Legal Document Analyzer Backend

A modular Python backend system for AI-powered legal document analysis using an agent-based architecture. The system uses Groq API for fast LLM inference and is designed to be fully extensible.

## Features

- Document analysis for PDF and DOCX files
- Multiple specialized agents for different aspects of legal document analysis
- Fast LLM inference using Groq API
- RESTful API endpoints for document processing
- Extensible agent-based architecture
- Support for custom compliance rules and clause templates

## Agents

1. **SupervisorAgent**: Manages the flow and coordinates other agents
2. **ReviewAgent**: Extracts legal terms, parties, dates, and obligations
3. **RiskAnalysisAgent**: Detects vague, risky, or ambiguous clauses
4. **ClauseComparisonAgent**: Compares clauses to standard templates
5. **SuggestionAgent**: Rewrites clauses with safer alternatives
6. **InconsistencyAgent**: Flags conflicting terms and inconsistencies
7. **ComplianceAgent**: Checks for jurisdictional legal compliance
8. **SummaryAgent**: Generates concise, structured summaries

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:
   - `POST /analyze/document`: Upload and analyze a document (PDF/DOCX)
   - `POST /analyze/text`: Analyze text content directly
   - `GET /health`: Health check endpoint

4. API Documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── supervisor_agent.py
│   ├── review_agent.py
│   ├── risk_analysis_agent.py
│   ├── clause_comparison_agent.py
│   ├── suggestion_agent.py
│   ├── inconsistency_agent.py
│   ├── compliance_agent.py
│   └── summary_agent.py
├── data/
│   ├── clause_templates/
│   └── compliance_rules/
├── main.py
├── requirements.txt
└── README.md
```

## Adding Custom Templates and Rules

1. Clause Templates:
   - Add JSON files to `data/clause_templates/`
   - Each template should include:
     - Template name
     - Template text
     - Required elements
     - Optional elements
     - Usage guidelines

2. Compliance Rules:
   - Add JSON files to `data/compliance_rules/`
   - Each rule set should include:
     - Jurisdiction
     - Applicable laws
     - Requirements
     - Compliance criteria
     - Penalties

## Extending the System

1. Creating a New Agent:
   - Inherit from `BaseAgent`
   - Implement the `process` method
   - Add the agent to `SupervisorAgent`

2. Adding New Features:
   - Create new agent classes
   - Update the supervisor agent
   - Add new API endpoints if needed

## Error Handling

The system includes comprehensive error handling:
- File processing errors
- API request validation
- LLM interaction errors
- Agent processing errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 