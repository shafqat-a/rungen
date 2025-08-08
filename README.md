# AutoGen with Groq Models

This project demonstrates how to use Microsoft AutoGen with Groq's high-performance language models for multi-agent conversations and automation.

## Features

- 🚀 Easy integration with Groq's fast inference API
- 🤖 Multiple agent types (assistant, code reviewer, planner)
- 💬 Group chat capabilities with multiple specialized agents
- 🔧 Configurable model parameters and settings
- 📊 Support for all major Groq models (Llama 3.1, Mixtral, Gemma 2)

## Available Groq Models

| Model | Parameters | Context Window | Best For |
|-------|------------|----------------|----------|
| llama-3.1-405b-reasoning | 405B | 131,072 | Complex reasoning, analysis |
| llama-3.1-70b-versatile | 70B | 131,072 | General purpose, coding |
| llama-3.1-8b-instant | 8B | 131,072 | Quick responses, high throughput |
| mixtral-8x7b-32768 | 8x7B | 32,768 | Coding, technical tasks |
| gemma2-9b-it | 9B | 8,192 | Instruction following, chat |

## Setup

### 1. Get Groq API Key

1. Sign up at [Groq Console](https://console.groq.com/)
2. Navigate to the API Keys section
3. Create a new API key
4. Copy your API key

### 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or install individually
pip install pyautogen groq matplotlib pandas
```

### 3. Set Environment Variable

```bash
# Option 1: Export in your shell
export GROQ_API_KEY='your-groq-api-key-here'

# Option 2: Add to your shell profile
echo 'export GROQ_API_KEY="your-groq-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Option 3: Use a .env file (create .env in project root)
echo 'GROQ_API_KEY=your-groq-api-key-here' > .env
```

## Usage

### Quick Start

```python
from models import GroqModelConfig, create_sample_agents

# Initialize Groq configuration
groq_config = GroqModelConfig()

# Create agents
user_proxy, assistant = create_sample_agents(groq_config, "llama-3.1-70b-versatile")

# Start a conversation
user_proxy.initiate_chat(
    assistant,
    message="Help me write a Python function to calculate Fibonacci numbers.",
    max_turns=3
)
```

### Run Examples

```bash
# Run all examples
python example.py

# Or just test the model configuration
python models.py
```

### Custom Configuration

```python
from models import GroqModelConfig
from autogen import AssistantAgent, UserProxyAgent

# Create custom configuration
groq_config = GroqModelConfig()
config = groq_config.create_autogen_config("llama-3.1-405b-reasoning")

# Customize parameters
config["temperature"] = 0.3  # More deterministic responses
config["config_list"][0]["max_tokens"] = 8192  # Longer responses

# Create custom agent
assistant = AssistantAgent(
    name="data_scientist",
    llm_config=config,
    system_message="You are an expert data scientist specializing in machine learning."
)
```

## Project Structure

```
rungen/
├── models.py          # Groq model configuration and utilities
├── example.py         # Example implementations and demos
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── workspace/        # AutoGen workspace directory (auto-created)
```

## Examples Included

### 1. Simple Conversation
Basic chat between user and assistant agent using Groq models.

### 2. Code Review
Specialized agent that reviews code for bugs, best practices, and improvements.

### 3. Multi-Agent Collaboration
Multiple specialized agents (planner, coder, reviewer) working together on a task.

## Model Selection Guide

- **llama-3.1-405b-reasoning**: Use for complex analysis, research, and reasoning tasks
- **llama-3.1-70b-versatile**: Best general-purpose model for most applications
- **llama-3.1-8b-instant**: When you need fast responses and have simpler tasks
- **mixtral-8x7b-32768**: Excellent for coding and technical documentation
- **gemma2-9b-it**: Good for instruction-following and structured conversations

## Advanced Features

### Group Chat with Role-Based Agents

```python
from autogen import GroupChat, GroupChatManager

# Create specialized agents
planner = AssistantAgent(name="planner", ...)
developer = AssistantAgent(name="developer", ...)
tester = AssistantAgent(name="tester", ...)

# Set up group chat
groupchat = GroupChat(
    agents=[user_proxy, planner, developer, tester],
    messages=[],
    max_round=20
)

manager = GroupChatManager(groupchat=groupchat, llm_config=config)
```

### Custom Agent with Tools

```python
# Agent with code execution capabilities
code_executor = UserProxyAgent(
    name="code_executor",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": True,  # Safer code execution
    }
)
```

## Performance Tips

1. **Model Selection**: Use faster models (8B) for simple tasks, larger models (70B, 405B) for complex reasoning
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Context Management**: Monitor token usage with longer conversations
4. **Batch Processing**: Process multiple requests in parallel when possible

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure `GROQ_API_KEY` is set correctly
2. **Rate Limits**: Groq has generous rate limits, but add delays if needed
3. **Model Availability**: Some models may have limited availability during peak times
4. **Context Length**: Monitor message length to stay within model limits

### Error Handling

```python
try:
    groq_config = GroqModelConfig()
    # Your code here
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Runtime error: {e}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Groq Models](https://console.groq.com/docs/models)
- [AutoGen Examples](https://github.com/microsoft/autogen/tree/main/notebook)

## Support

For issues with:
- **AutoGen**: Check the [AutoGen GitHub repository](https://github.com/microsoft/autogen)
- **Groq API**: Visit [Groq Support](https://console.groq.com/docs/support)
- **This Project**: Open an issue in this repository
