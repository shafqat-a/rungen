"""
Test script for AutoGen with Groq models (new version)
This script tests the integration with the newer AutoGen version.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_basic_import():
    """Test basic AutoGen imports"""
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        print("✅ AutoGen imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_groq_connection():
    """Test basic connection to Groq"""
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from autogen_core.models import ModelInfo, ModelFamily
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not found in environment")
            return False
        
        # Create model info for Groq models
        model_info = ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
            structured_output=True,
        )
        
        # Create client
        client = OpenAIChatCompletionClient(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            model_info=model_info,
        )
        
        print("✅ Groq client created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Groq connection error: {e}")
        return False

async def test_simple_agent():
    """Test creating and using a simple agent"""
    try:
        from models import create_assistant_agent
        
        # Create agent
        agent = create_assistant_agent(
            name="TestAgent",
            model="llama-3.1-8b-instant",
            system_message="You are a helpful test assistant. Keep responses brief."
        )
        
        print("✅ Agent created successfully")
        print(f"   Agent name: {agent.name}")
        print(f"   Agent description: {agent.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

async def test_simple_chat():
    """Test a simple chat interaction"""
    try:
        from models import create_assistant_agent
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_agentchat.ui import Console
        
        # Create agent
        agent = create_assistant_agent(
            name="ChatBot",
            model="llama-3.1-8b-instant",
            system_message="You are a helpful assistant. Respond with exactly one short sentence."
        )
        
        # Create team
        team = RoundRobinGroupChat([agent])
        
        print("🚀 Testing simple chat...")
        
        # Simple test message
        result = await Console(
            team.run_stream(task="Say hello in exactly 5 words.")
        )
        
        print("✅ Chat test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Testing AutoGen with Groq Integration")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_import),
        ("Groq Connection", test_groq_connection), 
        ("Agent Creation", test_simple_agent),
        ("Simple Chat", test_simple_chat),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your AutoGen + Groq setup is working!")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())
