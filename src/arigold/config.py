"""
Configuration management for the Arigold agent.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Configuration for the Arigold orchestrating agent."""

    model_config = SettingsConfigDict(env_prefix="ARIGOLD_", case_sensitive=False)

    # Google Cloud Configuration
    project_id: str = "jrw-demo-project"
    location: str = "us-central1"
    region: str = "us-central1"
    
    # Google API Authentication
    api_key: str
    
    # Agent Configuration
    agent_name: str = "Ari Gold Super Agent"
    agent_description: str = "An orchestrating agent that coordinates multiple specialized agents"
    
    # Model Configuration
    model_name: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 512
    
    # Logging
    log_level: str = "INFO"
    
    # Cloud Functions Deployment
    function_name: str = "arigold-agent"


# Global config instance
config = AgentConfig()
