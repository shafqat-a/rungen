"""
Multi-Provider Model Configuration for AutoGen
Supports Groq, OpenAI, Google Gemini, Anthropic Claude, and other providers
"""

import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily

# Load environment variables
load_dotenv()

class MultiProviderConfig:
    """Configuration class for multiple AI model providers"""
    
    def __init__(self):
        # Load API keys
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPEN_AI_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPKEY_API_KEY")
        
        # Provider configurations
        self.providers = {
            "groq": {
                "base_url": "https://api.groq.com/openai/v1",
                "api_key": self.groq_api_key,
                "models": {
                    "llama-3.3-70b-versatile": "Llama 3.3 70B - Most capable",
                    "llama-3.1-70b-versatile": "Llama 3.1 70B - Most capable, slower",
                    "llama-3.1-8b-instant": "Llama 3.1 8B - Fast and efficient",
                    "mixtral-8x7b-32768": "Mixtral 8x7B - Good for complex reasoning",
                    "gemma2-9b-it": "Gemma 2 9B - Instruction tuned",
                }
            },
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "api_key": self.openai_api_key,
                "models": {
                    "gpt-4": "GPT-4 - Most capable OpenAI model",
                    "gpt-4-turbo": "GPT-4 Turbo - Fast and capable",
                    "gpt-3.5-turbo": "GPT-3.5 Turbo - Fast and efficient",
                }
            },
            "moonshot": {
                "base_url": "https://api.moonshot.cn/v1",
                "api_key": self.openai_api_key,  # Often uses OpenAI-compatible key
                "models": {
                    "moonshot-v1-8k": "Moonshot v1 8K context",
                    "moonshot-v1-32k": "Moonshot v1 32K context", 
                    "moonshot-v1-128k": "Moonshot v1 128K context",
                    "moonshotai/kimi-k2-instruct": "Kimi K2 Instruct model",
                }
            },
            "deepseek": {
                "base_url": "https://api.deepseek.com/v1",
                "api_key": self.deepseek_api_key,
                "models": {
                    "deepseek-chat": "DeepSeek Chat model",
                    "deepseek-coder": "DeepSeek Coder model",
                    "deepseek-r1-distill-llama-70b": "DeepSeek R1 Distill Llama 70B",
                }
            },
            "google": {
                "base_url": None,  # Uses Google's SDK
                "api_key": self.google_api_key,
                "models": {
                    "gemini-1.5-pro": "Gemini 1.5 Pro - Most capable",
                    "gemini-1.5-flash": "Gemini 1.5 Flash - Fast",
                    "gemini-2.0-flash-exp": "Gemini 2.0 Flash Experimental",
                    "gemini-2.5-pro": "Gemini 2.5 Pro - Latest",
                }
            }
        }
    
    def get_client(self, model_name, provider=None):
        """Get client for any supported model"""
        if provider is None:
            # Auto-detect provider from model name
            provider = self._detect_provider(model_name)
        
        if provider == "google":
            return self._get_google_client(model_name)
        else:
            return self._get_openai_compatible_client(model_name, provider)
    
    def _detect_provider(self, model_name):
        """Auto-detect provider from model name"""
        for provider, config in self.providers.items():
            if model_name in config["models"]:
                return provider
        
        # Default fallbacks based on model name patterns
        if "gemini" in model_name.lower():
            return "google"
        elif "gpt" in model_name.lower():
            return "openai"
        elif "llama" in model_name.lower() or "mixtral" in model_name.lower():
            return "groq"
        elif "moonshot" in model_name.lower() or "kimi" in model_name.lower():
            return "moonshot"
        elif "deepseek" in model_name.lower():
            return "deepseek"
        else:
            return "groq"  # Default fallback
    
    def _get_openai_compatible_client(self, model_name, provider):
        """Get OpenAI-compatible client for Groq, OpenAI, Moonshot, DeepSeek"""
        config = self.providers[provider]
        
        if not config["api_key"]:
            raise ValueError(f"{provider.upper()}_API_KEY not found in environment variables")
        
        # Create model info
        model_info = ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
            structured_output=True,
        )
        
        return OpenAIChatCompletionClient(
            model=model_name,
            api_key=config["api_key"],
            base_url=config["base_url"],
            model_info=model_info,
        )
    
    def _get_google_client(self, model_name):
        """Get Google Gemini client"""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # For now, we'll use OpenAI-compatible approach for Gemini
        # In a full implementation, you'd use the Google SDK directly
        model_info = ModelInfo(
            vision=True,  # Gemini supports vision
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
            structured_output=True,
        )
        
        # Note: This is a simplified approach. For full Gemini support,
        # you'd need to implement a custom client using google-generativeai
        return OpenAIChatCompletionClient(
            model=model_name,
            api_key=self.google_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            model_info=model_info,
        )

def create_agent(name, model, system_message, provider=None):
    """Create an AutoGen agent with any supported model"""
    config = MultiProviderConfig()
    
    return AssistantAgent(
        name=name,
        description=f"An AI agent powered by {model}",
        system_message=system_message,
        model_client=config.get_client(model, provider),
    )

# Orion1 Team Models
ORION1_MODELS = {
    "principal_decision_maker": "llama-3.3-70b-versatile",
    "product_manager": "llama-3.3-70b-versatile", 
    "software_architect": "gemini-2.5-pro",
    "software_developer": "moonshotai/kimi-k2-instruct",
    "software_tester": "deepseek-r1-distill-llama-70b",
}

def create_orion1_team():
    """Create the complete Orion1 software development team"""
    
    # 1. Principal Decision Maker
    principal = create_agent(
        name="Principal_DecisionMaker",
        model=ORION1_MODELS["principal_decision_maker"],
        system_message="""You are the Principal Decision Maker for Orion1 software team.
        Your role is to:
        - Make final strategic and technical decisions
        - Resolve conflicts between team members
        - Ensure project alignment with business goals
        - Approve major architectural changes
        - Manage project timeline and priorities
        
        Keep decisions clear, well-reasoned, and actionable.""",
        provider="groq"
    )
    
    # 2. Product Manager
    product_manager = create_agent(
        name="Product_Manager",
        model=ORION1_MODELS["product_manager"],
        system_message="""You are the Product Manager for Orion1 software team.
        Your role is to:
        - Define product requirements and user stories
        - Prioritize features and backlog items
        - Communicate with stakeholders
        - Ensure user experience is optimal
        - Track project progress and deliverables
        
        Focus on user value and business impact.""",
        provider="groq"
    )
    
    # 3. Software Architect
    architect = create_agent(
        name="Software_Architect",
        model=ORION1_MODELS["software_architect"],
        system_message="""You are the Software Architect for Orion1 software team.
        Your role is to:
        - Design system architecture and technical solutions
        - Make technology stack decisions
        - Ensure scalability, security, and maintainability
        - Create technical documentation and diagrams
        - Review and approve architectural changes
        
        Think systematically about long-term technical health.""",
        provider="google"
    )
    
    # 4. Software Developer 1
    developer1 = create_agent(
        name="Software_Developer_1",
        model=ORION1_MODELS["software_developer"],
        system_message="""You are Software Developer 1 for Orion1 software team.
        Your role is to:
        - Implement features according to specifications
        - Write clean, maintainable, and efficient code
        - Participate in code reviews
        - Debug and fix issues
        - Collaborate with other developers
        
        Focus on code quality and best practices.""",
        provider="moonshot"
    )
    
    # 5. Software Developer 2  
    developer2 = create_agent(
        name="Software_Developer_2",
        model=ORION1_MODELS["software_developer"],
        system_message="""You are Software Developer 2 for Orion1 software team.
        Your role is to:
        - Implement features according to specifications
        - Write clean, maintainable, and efficient code
        - Participate in code reviews
        - Debug and fix issues
        - Collaborate with other developers
        
        Focus on performance optimization and user experience.""",
        provider="moonshot"
    )
    
    # 6. Software Tester (Playwright Expert)
    tester = create_agent(
        name="Software_Tester",
        model=ORION1_MODELS["software_tester"],
        system_message="""You are the Software Tester for Orion1 software team with expertise in Playwright.
        Your role is to:
        - Design and implement comprehensive test strategies
        - Write automated tests using Playwright for web applications
        - Perform manual testing when needed
        - Create test cases and documentation
        - Report bugs and verify fixes
        - Ensure quality standards are met
        
        Expertise areas: Playwright, E2E testing, API testing, performance testing.""",
        provider="deepseek"
    )
    
    return {
        "principal_decision_maker": principal,
        "product_manager": product_manager,
        "software_architect": architect,
        "software_developer_1": developer1,
        "software_developer_2": developer2,
        "software_tester": tester,
    }

# Available models across all providers
ALL_MODELS = {}
for provider, config in MultiProviderConfig().providers.items():
    for model, description in config["models"].items():
        ALL_MODELS[f"{provider}:{model}"] = description
