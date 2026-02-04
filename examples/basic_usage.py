"""
Example usage of the Arigold orchestrating agent.

This script demonstrates how to use the agent locally before deploying to Cloud Functions.
"""

import asyncio
import os

from arigold.agent import AgentOrchestrator


async def main():
    """Run example agent interactions."""
    print("=" * 60)
    print("Arigold - Orchestrating Agent Example")
    print("=" * 60)
    
    # Get API key from environment
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("\nWarning: GOOGLE_API_KEY not set in environment.")
        print("The agent may not work without proper authentication.")
    
    # Initialize the orchestrator
    print("\n1. Initializing the orchestrator...")
    orchestrator = AgentOrchestrator(api_key=api_key)
    
    # Example 1: Simple query
    print("\n2. Processing a simple query...")
    result = await orchestrator.process_request(
        "What can you help me with?",
        context={"user": "demo_user"}
    )
    response_text = result['response']
    if len(response_text) > 200:
        print(f"\nResponse: {response_text[:200]}...")
    else:
        print(f"\nResponse: {response_text}")
    print(f"Available agents: {result['agents_available']}")
    
    # Example 2: Register a sub-agent (mock)
    print("\n3. Registering a specialized sub-agent...")
    
    class MockDataAgent:
        """Mock data analysis agent."""
        def analyze(self, data):
            return {"status": "analyzed", "data": data}
    
    orchestrator.register_agent("data_analyzer", MockDataAgent())
    print(f"Registered agents: {orchestrator.list_agents()}")
    
    # Example 3: Query with multiple agents available
    print("\n4. Processing query with sub-agents available...")
    result = await orchestrator.process_request(
        "I need to analyze some data. Which agent should I use?",
        context={"task": "data_analysis"}
    )
    response_text = result['response']
    if len(response_text) > 200:
        print(f"\nResponse: {response_text[:200]}...")
    else:
        print(f"\nResponse: {response_text}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
