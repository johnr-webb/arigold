# Ari Gold - Super Agent

> "I am Ari Gold, and I am the best agent in the world" 

An orchestrating agent built with Google ADK (Agent Development Kit) that coordinates multiple specialized agents to accomplish complex tasks. Deploy it as a Google Cloud Function for scalable, serverless agent orchestration.

## Overview

Arigold is designed to be a "super agent" that can:
- Coordinate multiple specialized sub-agents
- Delegate tasks to the appropriate agent based on requirements
- Process complex requests that require multiple steps
- Scale automatically on Google Cloud Functions
- Provide a simple HTTP API for agent interactions

## Features

- 🤖 **Agent Orchestration**: Coordinate multiple specialized agents
- 🔌 **Extensible Architecture**: Easy to register and manage sub-agents
- ☁️ **Cloud-Native**: Built for Google Cloud Functions deployment
- 🎯 **Google ADK Integration**: Uses Google's Generative AI API
- 📊 **Context-Aware**: Process requests with rich context
- 🔐 **Secure**: Environment-based configuration with secret management
- 🚀 **Scalable**: Automatic scaling with Cloud Functions

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Cloud account
- Google API key or service account with Generative AI API access
- gcloud CLI (for deployment)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/johnr-webb/arigold.git
cd arigold
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
```bash
export GOOGLE_API_KEY="your-api-key-here"
export ARIGOLD_PROJECT_ID="your-gcp-project-id"
```

### Local Testing

Run the example script to test the agent locally:

```bash
python examples/basic_usage.py
```

### Deployment to Google Cloud Functions

1. Configure your project settings:
```bash
export ARIGOLD_PROJECT_ID="your-gcp-project-id"
export ARIGOLD_REGION="us-central1"
export ARIGOLD_FUNCTION_NAME="arigold-agent"
```

2. Deploy the function:
```bash
./scripts/deploy.sh
```

3. Test the deployed function:
```bash
./scripts/test_function.sh
```

## Usage

### As a Python Library

```python
from arigold.agent import AgentOrchestrator

# Initialize the orchestrator
orchestrator = AgentOrchestrator(api_key="your-api-key")

# Register specialized agents
orchestrator.register_agent("data_analyzer", DataAnalyzerAgent())
orchestrator.register_agent("text_processor", TextProcessorAgent())

# Process a request
result = orchestrator.process_request_sync(
    "Analyze this data and generate a report",
    context={"user_id": "user123", "task_type": "analysis"}
)

print(result["response"])
```

### As an HTTP API

Once deployed, send POST requests to your Cloud Function:

```bash
curl -X POST https://your-function-url \
  -H "Content-Type: application/json" \
  -d '{
    "request": "What agents are available?",
    "context": {"user": "demo"}
  }'
```

## Architecture

### Project Structure

```
arigold/
├── src/
│   └── arigold/
│       ├── __init__.py          # Package initialization
│       ├── config.py            # Configuration management
│       ├── agent.py             # Core orchestrator implementation
│       └── main.py              # Cloud Functions entry point
├── examples/
│   └── basic_usage.py           # Usage examples
├── scripts/
│   ├── deploy.sh                # Deployment script
│   └── test_function.sh         # Testing script
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Key Components

1. **AgentOrchestrator**: The main orchestrating agent that coordinates sub-agents
2. **AgentConfig**: Configuration management with environment variable support
3. **Cloud Functions Handler**: HTTP endpoint for serverless deployment
4. **Sub-Agent Registry**: Extensible system for registering specialized agents

## Configuration

Configuration is managed through environment variables with the `ARIGOLD_` prefix:

| Variable | Description | Default |
|----------|-------------|---------|
| `ARIGOLD_PROJECT_ID` | Google Cloud project ID | "" |
| `ARIGOLD_LOCATION` | Google Cloud region | "us-central1" |
| `ARIGOLD_AGENT_NAME` | Name of the orchestrator | "Arigold Orchestrator" |
| `ARIGOLD_MODEL_NAME` | Google GenAI model to use | "gemini-2.0-flash-exp" |
| `ARIGOLD_TEMPERATURE` | Model temperature (0-1) | 0.7 |
| `ARIGOLD_MAX_TOKENS` | Maximum output tokens | 8192 |
| `ARIGOLD_LOG_LEVEL` | Logging level | "INFO" |
| `GOOGLE_API_KEY` | Google API key for authentication | - |

## Extending Arigold

### Adding a Custom Sub-Agent

```python
class CustomAgent:
    """Your custom specialized agent."""
    
    def process(self, task):
        # Your agent logic here
        return {"result": "processed"}

# Register it with the orchestrator
orchestrator = AgentOrchestrator()
orchestrator.register_agent("custom_agent", CustomAgent())
```

### Creating Agent-Specific Logic

The orchestrator automatically includes information about available agents in its system prompt, allowing it to intelligently delegate tasks.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
ruff check src/
```

## Security

- Store sensitive credentials (API keys) in Google Secret Manager
- Use service accounts with minimal required permissions
- Enable authentication on Cloud Functions in production
- Review and configure CORS settings appropriately

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using Google ADK
