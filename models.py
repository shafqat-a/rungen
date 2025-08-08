"""
AutoGen Model Configuration for Groq
This file contains the model configurations for using AutoGen with Groq.
"""

import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily

# Load environment variables
load_dotenv()

class GroqConfig:
    """Configuration class for Groq models"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.base_url = "https://api.groq.com/openai/v1"
        self.default_model = os.getenv("DEFAULT_GROQ_MODEL", "llama-3.1-70b-versatile")
    
    def get_client(self, model_name=None):
        """Get OpenAI-compatible client for Groq"""
        if model_name is None:
            model_name = self.default_model
        
        # Create model info for Groq models
        model_info = ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
            structured_output=True,
        )
        
        return OpenAIChatCompletionClient(
            model=model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            model_info=model_info,
        )

# Available Groq models
GROQ_MODELS = {
    "llama-3.1-70b-versatile": "Llama 3.1 70B - Most capable, slower",
    "llama-3.1-8b-instant": "Llama 3.1 8B - Fast and efficient", 
    "mixtral-8x7b-32768": "Mixtral 8x7B - Good for complex reasoning",
    "gemma2-9b-it": "Gemma 2 9B - Instruction tuned",
    "llama3-70b-8192": "Llama 3 70B - High quality responses",
    "llama3-8b-8192": "Llama 3 8B - Fast responses",
}

def create_assistant_agent(name="Assistant", model="llama-3.1-70b-versatile", system_message=None):
    """Create an AutoGen assistant agent with Groq model"""
    groq_config = GroqConfig()
    
    if system_message is None:
        system_message = f"You are a helpful AI assistant named {name}."
    
    return AssistantAgent(
        name=name,
        description=f"An AI assistant powered by {model}",
        system_message=system_message,
        model_client=groq_config.get_client(model),
    )

# For backward compatibility with older AutoGen examples
def get_groq_config_list():
    """Get configuration list in the older AutoGen format (for compatibility)"""
    groq_config = GroqConfig()
    return [
        {
            "model": "llama-3.1-70b-versatile",
            "api_key": groq_config.api_key,
            "base_url": groq_config.base_url,
            "api_type": "openai",
        },
        {
            "model": "llama-3.1-8b-instant", 
            "api_key": groq_config.api_key,
            "base_url": groq_config.base_url,
            "api_type": "openai",
        },
        {
            "model": "mixtral-8x7b-32768",
            "api_key": groq_config.api_key,
            "base_url": groq_config.base_url,
            "api_type": "openai",
        },
    ]

import os
from typing import Dict, Any, List


class GroqModelConfig:
    """Configuration class for Groq models."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Groq model configuration.
        
        Args:
            api_key (str, optional): Groq API key. If not provided, will look for GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable must be set or api_key must be provided")
    
    def get_model_config(self, model_name: str = "llama-3.1-70b-versatile") -> List[Dict[str, Any]]:
        """
        Get the model configuration for AutoGen.
        
        Args:
            model_name (str): The Groq model to use. Default is 'llama-3.1-70b-versatile'.
        
        Returns:
            List[Dict[str, Any]]: Model configuration for AutoGen
        """
        return [
            {
                "model": model_name,
                "api_key": self.api_key,
                "base_url": "https://api.groq.com/openai/v1",
                "api_type": "openai",
                "temperature": 0.7,
                "max_tokens": 4096,
            }
        ]
    
    @staticmethod
    def get_available_models() -> Dict[str, Dict[str, Any]]:
        """
        Get a dictionary of available Groq models with their specifications.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of available models and their specs
        """
        return {
            "llama-3.1-405b-reasoning": {
                "description": "Meta's most capable model with 405B parameters, excellent for complex reasoning",
                "context_window": 131072,
                "max_tokens": 4096,
                "best_for": ["complex reasoning", "analysis", "problem solving"]
            },
            "llama-3.1-70b-versatile": {
                "description": "Balanced model with 70B parameters, good for most tasks",
                "context_window": 131072,
                "max_tokens": 4096,
                "best_for": ["general purpose", "coding", "conversation"]
            },
            "llama-3.1-8b-instant": {
                "description": "Fast and efficient model with 8B parameters",
                "context_window": 131072,
                "max_tokens": 4096,
                "best_for": ["quick responses", "simple tasks", "high throughput"]
            },
            "mixtral-8x7b-32768": {
                "description": "Mistral's mixture of experts model",
                "context_window": 32768,
                "max_tokens": 4096,
                "best_for": ["coding", "technical tasks", "analysis"]
            },
            "gemma2-9b-it": {
                "description": "Google's Gemma 2 model optimized for instruction following",
                "context_window": 8192,
                "max_tokens": 4096,
                "best_for": ["instruction following", "chat", "simple tasks"]
            }
        }
    
    @staticmethod
    def print_available_models():
        """Print information about available Groq models."""
        models = GroqModelConfig.get_available_models()
        print("Available Groq Models:")
        print("=" * 50)
        
        for model_id, specs in models.items():
            print(f"\nModel: {model_id}")
            print(f"Description: {specs['description']}")
            print(f"Context Window: {specs['context_window']:,} tokens")
            print(f"Max Output: {specs['max_tokens']:,} tokens")
            print(f"Best for: {', '.join(specs['best_for'])}")
    
    def create_autogen_config(self, model_name: str = "llama-3.1-70b-versatile") -> Dict[str, Any]:
        """
        Create a complete AutoGen configuration with the specified Groq model.
        
        Args:
            model_name (str): The Groq model to use
        
        Returns:
            Dict[str, Any]: Complete AutoGen configuration
        """
        return {
            "config_list": self.get_model_config(model_name),
            "timeout": 120,
            "temperature": 0.7,
            "cache_seed": None,  # Set to an integer for reproducible results
        }


def create_sample_agents(groq_config: GroqModelConfig, model_name: str = "llama-3.1-70b-versatile"):
    """
    Create sample AutoGen agents using Groq models.
    
    Args:
        groq_config (GroqModelConfig): Groq configuration instance
        model_name (str): The model to use for the agents
    
    Returns:
        tuple: (user_proxy, assistant) agents
    """
    from autogen import UserProxyAgent, AssistantAgent
    
    # Get the model configuration
    config = groq_config.create_autogen_config(model_name)
    
    # Create a user proxy agent
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",  # Change to "ALWAYS" for interactive mode
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False,  # Set to True if you have Docker installed
        },
    )
    
    # Create an assistant agent
    assistant = AssistantAgent(
        name="assistant",
        llm_config=config,
        system_message="""You are a helpful AI assistant powered by Groq. 
        You can help with coding, analysis, and problem-solving tasks.
        When you have completed a task, reply with TERMINATE."""
    )
    
    return user_proxy, assistant


if __name__ == "__main__":
    # Example usage
    print("Groq Model Configuration for AutoGen")
    print("=" * 40)
    
    # Print available models
    GroqModelConfig.print_available_models()
    
    # Example of creating configuration (requires GROQ_API_KEY environment variable)
    try:
        groq_config = GroqModelConfig()
        config = groq_config.create_autogen_config("llama-3.1-70b-versatile")
        print(f"\nExample configuration created successfully!")
        print(f"Model: {config['config_list'][0]['model']}")
        print(f"Base URL: {config['config_list'][0]['base_url']}")
    except ValueError as e:
        print(f"\nTo use this configuration, set your GROQ_API_KEY environment variable:")
        print(f"export GROQ_API_KEY='your-groq-api-key-here'")
