"""
Simple example demonstrating AutoGen with Groq models.
This script shows how to set up and use AutoGen agents with Groq's language models.
"""

import os
import sys
from models import GroqModelConfig, create_sample_agents


def setup_environment():
    """Set up the environment for running AutoGen with Groq."""
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY environment variable is not set!")
        print("\nTo get started:")
        print("1. Sign up at https://console.groq.com/")
        print("2. Get your API key from the dashboard")
        print("3. Set the environment variable:")
        print("   export GROQ_API_KEY='your-groq-api-key-here'")
        print("\nOr run this script with:")
        print("   GROQ_API_KEY='your-key' python example.py")
        return False
    
    # Create workspace directory
    os.makedirs("workspace", exist_ok=True)
    return True


def run_simple_conversation():
    """Run a simple conversation between AutoGen agents using Groq."""
    print("🚀 Starting AutoGen with Groq models...")
    
    try:
        # Initialize Groq configuration
        groq_config = GroqModelConfig()
        
        # Create agents using Llama 3.1 70B model
        user_proxy, assistant = create_sample_agents(groq_config, "llama-3.1-70b-versatile")
        
        # Start a conversation
        print("\n💬 Starting conversation...")
        print("=" * 50)
        
        # Example: Ask the assistant to write a simple Python function
        message = """
        Write a Python function that calculates the factorial of a number.
        Include error handling for negative numbers and non-integers.
        Also write a few test cases to demonstrate it works correctly.
        """
        
        user_proxy.initiate_chat(
            assistant,
            message=message,
            max_turns=3
        )
        
        print("\n✅ Conversation completed!")
        
    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        return False
    
    return True


def run_code_review_example():
    """Example of using AutoGen for code review with Groq."""
    print("\n🔍 Code Review Example with AutoGen + Groq")
    print("=" * 50)
    
    try:
        groq_config = GroqModelConfig()
        
        # Create a specialized code reviewer agent
        from autogen import AssistantAgent, UserProxyAgent
        
        config = groq_config.create_autogen_config("llama-3.1-70b-versatile")
        
        code_reviewer = AssistantAgent(
            name="code_reviewer",
            llm_config=config,
            system_message="""You are an expert code reviewer. 
            Analyze the provided code for:
            1. Bugs and potential issues
            2. Code quality and best practices
            3. Performance improvements
            4. Security concerns
            5. Readability and maintainability
            
            Provide specific, actionable feedback.
            End your review with TERMINATE."""
        )
        
        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )
        
        # Code to review
        code_to_review = '''
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
'''
        
        message = f"""
        Please review this Python code and provide feedback:
        
        ```python
        {code_to_review}
        ```
        """
        
        user_proxy.initiate_chat(code_reviewer, message=message)
        
    except Exception as e:
        print(f"❌ Error during code review: {e}")


def run_multi_agent_example():
    """Example with multiple specialized agents."""
    print("\n👥 Multi-Agent Example with AutoGen + Groq")
    print("=" * 50)
    
    try:
        groq_config = GroqModelConfig()
        config = groq_config.create_autogen_config("llama-3.1-70b-versatile")
        
        from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
        
        # Create specialized agents
        planner = AssistantAgent(
            name="planner",
            llm_config=config,
            system_message="""You are a project planner. Break down complex tasks into smaller, manageable steps.
            Create clear, actionable plans with priorities and dependencies."""
        )
        
        coder = AssistantAgent(
            name="coder",
            llm_config=config,
            system_message="""You are an expert programmer. Write clean, efficient, and well-documented code.
            Follow best practices and explain your implementation choices."""
        )
        
        reviewer = AssistantAgent(
            name="reviewer",
            llm_config=config,
            system_message="""You are a code reviewer. Analyze code for bugs, improvements, and best practices.
            Provide constructive feedback and suggestions."""
        )
        
        user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )
        
        # Create group chat
        groupchat = GroupChat(
            agents=[user_proxy, planner, coder, reviewer],
            messages=[],
            max_round=12,
            speaker_selection_method="round_robin"
        )
        
        manager = GroupChatManager(groupchat=groupchat, llm_config=config)
        
        # Start the group discussion
        task = """
        Create a Python script that:
        1. Reads a CSV file containing sales data
        2. Calculates monthly revenue totals
        3. Generates a simple bar chart visualization
        4. Saves the chart as a PNG file
        
        Please plan, implement, and review this solution.
        """
        
        user_proxy.initiate_chat(manager, message=task)
        
    except Exception as e:
        print(f"❌ Error in multi-agent example: {e}")


def main():
    """Main function to run AutoGen examples with Groq."""
    print("🤖 AutoGen + Groq Integration Examples")
    print("=" * 40)
    
    # Check environment setup
    if not setup_environment():
        return
    
    # Show available models
    print("\n📋 Available Groq Models:")
    GroqModelConfig.print_available_models()
    
    print("\n" + "="*60)
    print("RUNNING EXAMPLES")
    print("="*60)
    
    # Run examples
    examples = [
        ("Simple Conversation", run_simple_conversation),
        ("Code Review", run_code_review_example),
        ("Multi-Agent Collaboration", run_multi_agent_example),
    ]
    
    for name, func in examples:
        try:
            print(f"\n🎯 Running: {name}")
            func()
            print(f"✅ {name} completed successfully!")
        except KeyboardInterrupt:
            print(f"\n⚠️ {name} interrupted by user")
            break
        except Exception as e:
            print(f"❌ {name} failed: {e}")
        
        print("\n" + "-"*50)
    
    print("\n🎉 All examples completed!")
    print("\nNext steps:")
    print("- Modify the examples to suit your specific use case")
    print("- Experiment with different Groq models")
    print("- Try different temperature and max_tokens settings")
    print("- Add more specialized agents for your workflow")


if __name__ == "__main__":
    main()
