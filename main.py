"""
PharmacyGenius Search API
FastAPI application for drug search using GPT-4o Search Preview
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app with custom docs
app = FastAPI(
    title="PharmacyGenius Drug Search API",
    description="""
    ## PharmacyGenius Drug Search API with GPT-4o Search Preview
    
    A powerful drug search API that uses GPT-4o Search Preview to get real-time drug information from the web.
    
    * **Drug Search**: Search for comprehensive drug information from authoritative web sources
    * **Real-time Data**: Get the most up-to-date drug information from FDA, EMA, PubMed, and other sources
    * **Structured Results**: Receive well-formatted drug information including indications, dosage, side effects, and more
    * **AI-Powered**: Leverages GPT-4o's web search capabilities for accurate and comprehensive results
    
    ### Key Features:
    - Real-time web search using GPT-4o Search Preview
    - Structured drug information extraction
    - Sources from authoritative medical databases
    - Comprehensive drug profiles
    - RESTful API design
    
    ### Getting Started:
    1. Set your OpenAI API key in the environment variable `OPENAI_API_KEY`
    2. Use `/search/drug` endpoint with a drug name
    3. Get comprehensive drug information from web sources
    
    ### Example Usage:
    ```
    POST /search/drug
    {
        "drug_name": "aspirin"
    }
    ```
    """,
    version="1.0.0",
    contact={
        "name": "PharmacyGenius API Support",
        "email": "support@pharmacygenius.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai_client = OpenAI(api_key=api_key)
    else:
        print("Warning: OPENAI_API_KEY not found in environment variables")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")

# Pydantic Models
class DrugSearchRequest(BaseModel):
    """Request model for drug search"""
    drug_name: str = Field(..., min_length=1, max_length=100, description="Name of the drug to search for")
    include_dosage: bool = Field(True, description="Include dosage information")
    include_side_effects: bool = Field(True, description="Include side effects information")
    include_interactions: bool = Field(False, description="Include drug interactions")

class DrugInformation(BaseModel):
    """Structured drug information model"""
    name: str = Field(..., description="Drug name")
    generic_name: Optional[str] = Field(None, description="Generic name")
    brand_names: Optional[List[str]] = Field(None, description="Brand names")
    drug_class: Optional[str] = Field(None, description="Drug classification")
    indications: Optional[List[str]] = Field(None, description="Medical indications")
    mechanism_of_action: Optional[str] = Field(None, description="How the drug works")
    dosage: Optional[Dict[str, str]] = Field(None, description="Dosage information")
    side_effects: Optional[List[str]] = Field(None, description="Common side effects")
    contraindications: Optional[List[str]] = Field(None, description="Contraindications")
    drug_interactions: Optional[List[str]] = Field(None, description="Drug interactions")
    warnings: Optional[List[str]] = Field(None, description="Important warnings")
    formulations: Optional[List[str]] = Field(None, description="Available formulations")
    approval_status: Optional[str] = Field(None, description="FDA/regulatory approval status")
    sources: Optional[List[str]] = Field(None, description="Information sources")

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Any] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if any")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

def create_drug_search_prompt(drug_name: str, include_dosage: bool = True, include_side_effects: bool = True, include_interactions: bool = False) -> str:
    """Create a comprehensive prompt for drug information search"""
    
    base_prompt = f"""
    Search for comprehensive information about the drug "{drug_name}" and provide detailed, accurate information from authoritative medical sources. 

    Please provide the following information in a structured format:

    1. **Basic Information:**
       - Official drug name
       - Generic name (if applicable)
       - Common brand names
       - Drug classification/category

    2. **Medical Information:**
       - Primary indications (what conditions it treats)
       - Mechanism of action (how it works)
       - Therapeutic category

    3. **Regulatory Information:**
       - FDA approval status
       - Available formulations (tablets, injection, etc.)
       - Prescription vs OTC status
    """

    if include_dosage:
        base_prompt += """
    4. **Dosage Information:**
       - Typical adult dosage
       - Pediatric dosage (if applicable)
       - Administration route
       - Frequency of administration
        """

    if include_side_effects:
        base_prompt += """
    5. **Safety Information:**
       - Common side effects
       - Serious/rare side effects
       - Contraindications
       - Important warnings and precautions
        """

    if include_interactions:
        base_prompt += """
    6. **Drug Interactions:**
       - Major drug interactions
       - Food interactions
       - Alcohol interactions
        """

    base_prompt += """

    **Important Instructions:**
    - Only use information from authoritative medical sources (FDA, EMA, PubMed, medical textbooks, official drug labels)
    - Ensure all information is current and accurate
    - If certain information is not available or unclear, state that explicitly
    - Include the sources where you found this information
    - Format the response in clear, structured sections
    - Use medical terminology appropriately but explain complex terms

    Please search the web for the most current and accurate information about this drug.
    """

    return base_prompt

# Root endpoint
@app.get("/", response_model=Dict[str, str])
async def root():
    """
    API Root - Welcome endpoint
    """
    return {
        "message": "Welcome to PharmacyGenius Drug Search API",
        "version": "1.0.0",
        "powered_by": "GPT-4o Search Preview",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Health Check - Verify API and OpenAI connectivity
    """
    try:
        if not openai_client:
            return {
                "status": "warning",
                "openai_client": "not_configured",
                "message": "OpenAI API key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        # Test OpenAI connection with a simple request
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'API connection successful'"}],
            max_tokens=10
        )
        
        return {
            "status": "healthy",
            "openai_client": "connected",
            "model": "gpt-4o",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "openai_client": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Main drug search endpoint
@app.post("/search/drug", response_model=APIResponse, tags=["Drug Search"])
async def search_drug(request: DrugSearchRequest):
    """
    Search for Drug Information using GPT-4o Search Preview
    
    This endpoint uses GPT-4o's web search capabilities to find comprehensive, 
    up-to-date information about any drug from authoritative medical sources.
    
    **Features:**
    - Real-time web search from FDA, EMA, PubMed, and other medical databases
    - Structured drug information extraction
    - Comprehensive drug profiles including indications, dosage, side effects
    - Source attribution for all information
    
    **Example Request:**
    ```json
    {
        "drug_name": "lisinopril",
        "include_dosage": true,
        "include_side_effects": true,
        "include_interactions": false
    }
    ```
    
    **Response includes:**
    - Basic drug information (name, classification, brand names)
    - Medical information (indications, mechanism of action)
    - Dosage guidelines (if requested)
    - Safety information (if requested)
    - Drug interactions (if requested)
    - Regulatory status and formulations
    - Source attribution
    """
    if not openai_client:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI client not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    start_time = datetime.now()
    
    try:
        # Create the search prompt
        search_prompt = create_drug_search_prompt(
            drug_name=request.drug_name,
            include_dosage=request.include_dosage,
            include_side_effects=request.include_side_effects,
            include_interactions=request.include_interactions
        )
        
        # Use GPT-4o Search Preview for real-time web search
        response = openai_client.chat.completions.create(
            model="gpt-4o-search-preview",  # GPT-4o Search Preview model
            messages=[
                {
                    "role": "system", 
                    "content": "You are a medical information specialist. Search the web to find accurate, up-to-date drug information from authoritative medical sources like FDA, EMA, PubMed, and medical literature. Provide comprehensive, well-structured responses with source citations."
                },
                {
                    "role": "user", 
                    "content": search_prompt
                }
            ],
            max_tokens=2000
            # Note: temperature parameter not supported by search preview models
        )
        
        drug_info_text = response.choices[0].message.content
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Return structured response
        return APIResponse(
            success=True,
            data={
                "drug_name": request.drug_name,
                "search_query": search_prompt[:200] + "...",  # Truncated prompt for reference
                "drug_information": drug_info_text,
                "search_options": {
                    "include_dosage": request.include_dosage,
                    "include_side_effects": request.include_side_effects,
                    "include_interactions": request.include_interactions
                },
                "timestamp": start_time.isoformat()
            },
            message=f"Successfully retrieved information for '{request.drug_name}'",
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to search for drug information: {str(e)}"
        )

# Quick search endpoint (simplified)
@app.get("/search/quick", response_model=APIResponse, tags=["Drug Search"])
async def quick_drug_search(
    drug_name: str = Query(..., min_length=1, max_length=100, description="Name of the drug to search for")
):
    """
    Quick Drug Search
    
    A simplified endpoint for quick drug information lookup.
    Just provide the drug name as a query parameter.
    
    **Example:**
    `/search/quick?drug_name=aspirin`
    """
    # Convert to the main search format
    request = DrugSearchRequest(
        drug_name=drug_name,
        include_dosage=True,
        include_side_effects=True,
        include_interactions=False
    )
    
    return await search_drug(request)

# API Information endpoint
@app.get("/info", response_model=APIResponse, tags=["Information"])
async def api_info():
    """
    Get API Information
    
    Returns information about the API, its capabilities, and usage guidelines.
    """
    return APIResponse(
        success=True,
        data={
            "api_name": "PharmacyGenius Drug Search API",
            "version": "1.0.0",
            "powered_by": "GPT-4o Search Preview",
            "capabilities": [
                "Real-time web search for drug information",
                "Structured drug data extraction",
                "Authoritative source verification",
                "Comprehensive drug profiles",
                "Dosage and safety information",
                "Drug interaction checking"
            ],
            "endpoints": {
                "/search/drug": "Main drug search endpoint with detailed options",
                "/search/quick": "Quick drug search with drug name only",
                "/health": "API health check",
                "/info": "API information"
            },
            "data_sources": [
                "FDA (Food and Drug Administration)",
                "EMA (European Medicines Agency)",
                "PubMed",
                "Official drug labels",
                "Medical literature databases"
            ],
            "rate_limits": "Standard OpenAI API limits apply",
            "authentication": "OpenAI API key required"
        },
        message="API information retrieved successfully"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 