"""
Configuration management for the Arigold agent.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Configuration for the Arigold orchestrating agent."""

    model_config = SettingsConfigDict(env_prefix="ARIGOLD_", case_sensitive=False)

    # Google Cloud Configuration
    project_id: str = ""
    location: str = "us-central1"
    
    # Agent Configuration
    agent_name: str = "Arigold Orchestrator"
    agent_description: str = "An orchestrating agent that coordinates multiple specialized agents"
    
    # Model Configuration
    model_name: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 8192
    
    # Logging
    log_level: str = "INFO"


# Global config instance
config = AgentConfig()
