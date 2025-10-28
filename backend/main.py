"""
FastAPI Backend for AWS Career Guidance AI System
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import uvicorn

# Import the career guidance system
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from career_guidance_system import CareerGuidanceSystem, lambda_handler
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback to local import
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from career_guidance_system import CareerGuidanceSystem, lambda_handler

# Initialize FastAPI app
app = FastAPI(
    title="AWS Career Guidance AI System",
    description="AI-powered career guidance platform with multi-agent architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the career guidance system
career_system = CareerGuidanceSystem()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "AWS Career Guidance AI System API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        health_status = await career_system.health_check()
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/api/status")
async def get_system_status():
    """Get system status and configuration."""
    try:
        status = career_system.get_system_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/career-guidance")
async def get_career_guidance(request: Dict[str, Any]):
    """Main endpoint for career guidance queries."""
    try:
        query = request.get("query")
        session_id = request.get("sessionId")
        major = request.get("major")
        student_type = request.get("studentType")
        use_agent_core = request.get("useAgentCore", False)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        logger.info(f"Processing career guidance query: {query[:100]}...")
        logger.info(f"Context - Major: {major}, Student Type: {student_type}")
        logger.info(f"Using Agent Core: {use_agent_core}")
        
        # Set Agent Core usage for this request
        if use_agent_core:
            os.environ['USE_BEDROCK_AGENT_CORE'] = 'true'
        else:
            os.environ['USE_BEDROCK_AGENT_CORE'] = 'false'
        
        # Process the query through the career guidance system
        response = await career_system.process_query(query, session_id, major=major, student_type=student_type)
        
        # Convert response to dictionary for JSON serialization
        response_dict = {
            "query": response.user_query,
            "unified_response": response.unified_response,
            "job_market_insights": response.job_market_insights,
            "course_recommendations": response.course_recommendations,
            "career_matching_analysis": response.career_matching_analysis,
            "project_suggestions": response.project_suggestions,
            "session_id": response.session_id,
            "timestamp": response.timestamp,
            "used_agent_core": use_agent_core
        }
        
        logger.info(f"Successfully processed query for session {response.session_id}")
        return response_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing career guidance query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/sessions")
async def get_sessions():
    """Get all active sessions."""
    try:
        sessions = career_system.get_all_sessions()
        return {
            "sessions": sessions,
            "total_sessions": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific session by ID."""
    try:
        session = career_system.get_session_history(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific session."""
    try:
        success = career_system.clear_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session cleared successfully", "session_id": session_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to clear session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/sessions")
async def clear_all_sessions():
    """Clear all sessions."""
    try:
        career_system.clear_all_sessions()
        return {"message": "All sessions cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear all sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch-process")
async def batch_process(background_tasks: BackgroundTasks, request: Dict[str, Any]):
    """Process multiple queries in batch mode."""
    try:
        queries = request.get("queries", [])
        if not queries or not isinstance(queries, list):
            raise HTTPException(status_code=400, detail="Queries list is required")
        
        if len(queries) > 10:  # Limit batch size
            raise HTTPException(status_code=400, detail="Maximum 10 queries per batch")
        
        # Process queries in background
        background_tasks.add_task(process_batch_queries, queries)
        
        return {
            "message": "Batch processing started",
            "query_count": len(queries),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting batch processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_batch_queries(queries: list):
    """Background task to process batch queries."""
    results = []
    
    for i, query in enumerate(queries):
        try:
            logger.info(f"Processing batch query {i+1}/{len(queries)}: {query[:50]}...")
            response = await career_system.process_query(query)
            results.append({
                "query": query,
                "response": response.unified_response,
                "session_id": response.session_id,
                "timestamp": response.timestamp,
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error processing batch query {i+1}: {e}")
            results.append({
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            })
    
    # Save results to file
    import json
    output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Batch processing completed. Results saved to {output_file}")


@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all AI agents."""
    try:
        agents_status = {}
        
        # Test each agent
        agents = {
            "job_market": career_system.job_market_agent,
            "course_catalog": career_system.course_catalog_agent,
            "career_matching": career_system.career_matching_agent,
            "project_advisor": career_system.project_advisor_agent
        }
        
        for agent_name, agent in agents.items():
            try:
                # Simple health check
                agents_status[agent_name] = {
                    "status": "healthy",
                    "bedrock_client_available": agent.bedrock_client is not None,
                    "logger_configured": agent.logger is not None,
                    "agent_name": agent.agent_name
                }
            except Exception as e:
                agents_status[agent_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        return {
            "agents": agents_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get agents status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
