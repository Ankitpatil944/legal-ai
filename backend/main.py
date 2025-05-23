from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import fitz  # PyMuPDF
import docx
import os
from dotenv import load_dotenv
from agents.supervisor_agent import SupervisorAgent
import json
from pathlib import Path
import uvicorn
import tempfile
from docx import Document
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Initialize FastAPI app
app = FastAPI(title="Legal Document Analyzer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],  # Add both ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the supervisor agent
supervisor = SupervisorAgent()

class AnalysisRequest(BaseModel):
    document_text: str
    context: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    status: str
    results: Dict[str, Any]
    error: Optional[str] = None

async def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text from a PDF file."""
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            temp_path = temp_file.name
        # Now the file is closed, safe to open with fitz
        doc = fitz.open(temp_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        os.unlink(temp_path)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

async def extract_text_from_docx(file: UploadFile) -> str:
    """Extract text from a DOCX file."""
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            temp_path = temp_file.name
        # Now the file is closed, safe to open with python-docx
        doc = Document(temp_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        os.unlink(temp_path)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing DOCX: {str(e)}")

@app.post("/analyze/document", response_model=AnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    context: Optional[Dict[str, Any]] = None
):
    """
    Analyze a legal document (PDF or DOCX) and return the analysis results.
    """
    try:
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = await extract_text_from_pdf(file)
        elif file.filename.endswith(('.doc', '.docx')):
            text = await extract_text_from_docx(file)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF or DOCX file."
            )
        
        # Process the document using the supervisor agent
        results = await supervisor.process(text, context)
        
        return AnalysisResponse(
            status="success",
            results=results
        )
    except Exception as e:
        return AnalysisResponse(
            status="error",
            results={},
            error=str(e)
        )

@app.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    """
    Analyze text content directly and return the analysis results.
    """
    try:
        # Process the text using the supervisor agent
        results = await supervisor.process(request.document_text, request.context)
        
        return AnalysisResponse(
            status="success",
            results=results
        )
    except Exception as e:
        return AnalysisResponse(
            status="error",
            results={},
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

def print_startup_message():
    print("\n" + "="*80)
    print("\033[1mLegal Document Analyzer API\033[0m")
    print("="*80)
    print("\n\033[1mAvailable Agents:\033[0m")
    print("  • \033[1mSupervisorAgent\033[0m - Orchestrates the analysis process")
    print("  • \033[1mReviewAgent\033[0m - Extracts key legal information")
    print("  • \033[1mRiskAnalysisAgent\033[0m - Identifies risky clauses")
    print("  • \033[1mClauseComparisonAgent\033[0m - Compares against templates")
    print("  • \033[1mSuggestionAgent\033[0m - Generates safer alternatives")
    print("  • \033[1mInconsistencyAgent\033[0m - Flags conflicting terms")
    print("  • \033[1mComplianceAgent\033[0m - Checks legal compliance")
    print("  • \033[1mSummaryAgent\033[0m - Generates comprehensive summaries")
    print("\n\033[1mAPI Endpoints:\033[0m")
    print("  • POST /analyze/document - Upload and analyze documents")
    print("  • POST /analyze/text - Analyze text directly")
    print("  • GET /health - Health check endpoint")
    print("\n\033[1mServer Status:\033[0m")
    print(f"  • Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  • Running on: http://127.0.0.1:8000")
    print("="*80 + "\n")

if __name__ == "__main__":
    print_startup_message()
    uvicorn.run(app, host="127.0.0.1", port=8000) 