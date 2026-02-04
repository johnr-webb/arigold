"""
Core orchestrating agent implementation using Google ADK.

This module implements the main orchestrating agent that can coordinate
multiple specialized agents to accomplish complex tasks.
"""

import logging
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

from .config import config

# Configure logging
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    An orchestrating agent that coordinates multiple specialized agents.
    
    This agent uses Google's Generative AI API to process requests and
    can delegate tasks to other specialized agents as needed.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
    ):
        """
        Initialize the orchestrating agent.
        
        Args:
            api_key: Google API key for authentication
            project_id: Google Cloud project ID
            location: Google Cloud location
        """
        self.project_id = project_id or config.project_id
        self.location = location or config.location
        
        # Initialize the Google GenAI client
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
        
        self.model_name = config.model_name
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        
        # Registry of available sub-agents
        self.sub_agents: Dict[str, Any] = {}
        
        logger.info(
            f"Initialized {config.agent_name} with model {self.model_name}"
        )

    def register_agent(self, name: str, agent: Any) -> None:
        """
        Register a specialized sub-agent that can be delegated to.
        
        Args:
            name: Name identifier for the agent
            agent: The agent instance
        """
        self.sub_agents[name] = agent
        logger.info(f"Registered sub-agent: {name}")

    def list_agents(self) -> List[str]:
        """
        List all registered sub-agents.
        
        Returns:
            List of agent names
        """
        return list(self.sub_agents.keys())

    async def process_request(
        self,
        user_request: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process a user request and orchestrate sub-agents as needed.
        
        Args:
            user_request: The user's request or query
            context: Optional context information
            
        Returns:
            A dictionary containing the response and metadata
        """
        logger.info(f"Processing request: {user_request[:100]}...")
        
        # Build the system prompt for orchestration
        system_prompt = self._build_system_prompt()
        
        # Prepare the prompt with context
        full_prompt = self._prepare_prompt(user_request, context)
        
        try:
            # Generate response using Google GenAI
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    system_instruction=system_prompt,
                ),
            )
            
            # Extract and process the response
            result = {
                "response": response.text,
                "model": self.model_name,
                "agents_available": self.list_agents(),
                "context": context or {},
            }
            
            logger.info("Request processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "error": str(e),
                "response": "I encountered an error processing your request.",
                "agents_available": self.list_agents(),
            }

    def _build_system_prompt(self) -> str:
        """
        Build the system prompt for the orchestrating agent.
        
        Returns:
            The system prompt string
        """
        agent_list = ", ".join(self.sub_agents.keys()) if self.sub_agents else "none"
        
        return f"""You are {config.agent_name}, {config.agent_description}.

Your role is to understand user requests and coordinate with specialized agents when needed.

Available sub-agents: {agent_list}

When processing requests:
1. Analyze the user's request carefully
2. Determine if you can handle it directly or if a specialized agent is needed
3. If delegation is needed, explain which agent would be appropriate and why
4. Provide clear, helpful responses
5. Coordinate multiple agents if the task requires it

Always be helpful, clear, and efficient in your responses."""

    def _prepare_prompt(
        self,
        user_request: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Prepare the full prompt with context.
        
        Args:
            user_request: The user's request
            context: Optional context information
            
        Returns:
            The prepared prompt string
        """
        prompt_parts = []
        
        if context:
            prompt_parts.append("Context:")
            for key, value in context.items():
                prompt_parts.append(f"- {key}: {value}")
            prompt_parts.append("")
        
        prompt_parts.append(f"User Request: {user_request}")
        
        return "\n".join(prompt_parts)

    def process_request_sync(
        self,
        user_request: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous version of process_request for simpler use cases.
        
        Args:
            user_request: The user's request or query
            context: Optional context information
            
        Returns:
            A dictionary containing the response and metadata
        """
        import asyncio
        
        # Use asyncio.run() which properly handles loop creation and cleanup
        return asyncio.run(self.process_request(user_request, context))
