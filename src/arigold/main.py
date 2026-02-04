"""
Google Cloud Functions entry point for the Arigold agent.

This module provides the HTTP function handler for deploying
the agent as a Google Cloud Function.
"""

import json
import logging
import os
from typing import Any

import functions_framework
from flask import Request

from arigold.agent import AgentOrchestrator
from arigold.config import config

# Configure logging
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

# Initialize the orchestrator (reused across invocations)
orchestrator = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create the agent orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        orchestrator = AgentOrchestrator(api_key=api_key)
        logger.info("Orchestrator initialized")
    return orchestrator


@functions_framework.http
def arigold_agent(request: Request) -> tuple[str | dict, int] | tuple[str, int, dict]:
    """
    HTTP Cloud Function entry point for the Arigold agent.
    
    Args:
        request: Flask request object
        
    Returns:
        Tuple of (response_data, status_code) or (response_data, status_code, headers)
    """
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    try:
        # Parse the request
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return (
                json.dumps({"error": "No JSON body provided"}),
                400,
                headers,
            )
        
        # Extract parameters
        user_request = request_json.get("request", "")
        context = request_json.get("context", {})
        
        if not user_request:
            return (
                json.dumps({"error": "No 'request' field provided"}),
                400,
                headers,
            )
        
        # Process the request
        agent = get_orchestrator()
        result = agent.process_request_sync(user_request, context)
        
        return (json.dumps(result), 200, headers)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return (
            json.dumps({"error": f"Internal error: {str(e)}"}),
            500,
            headers,
        )


@functions_framework.http
def health_check(request: Request) -> tuple[str, int]:
    """
    Health check endpoint.
    
    Args:
        request: Flask request object
        
    Returns:
        Tuple of (response_data, status_code)
    """
    headers = {"Access-Control-Allow-Origin": "*"}
    return (
        json.dumps({"status": "healthy", "agent": config.agent_name}),
        200,
        headers,
    )
