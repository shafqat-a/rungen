"""
Quick test script to verify AutoGen + Groq integration is working.
Run this after setting your GROQ_API_KEY environment variable.
"""

import os
import sys
from models import GroqModelConfig


def test_groq_connection():
    """Test the Groq API connection and model configuration."""
    print("🧪 Testing Groq Connection...")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        print("\n📝 Setup instructions:")
        print("1. Get your API key from https://console.groq.com/")
        print("2. Run: export GROQ_API_KEY='your-api-key-here'")
        print("3. Run this test again: python test.py")
        return False
    
    print(f"✅ API key found: {api_key[:10]}..." + "*" * (len(api_key) - 10))
    
    try:
        # Test configuration creation
        groq_config = GroqModelConfig()
        print("✅ GroqModelConfig created successfully")
        
        # Test model config generation
        config = groq_config.create_autogen_config("llama-3.1-8b-instant")
        print("✅ AutoGen config generated successfully")
        
        print(f"📋 Config details:")
        print(f"   Model: {config['config_list'][0]['model']}")
        print(f"   Base URL: {config['config_list'][0]['base_url']}")
        print(f"   Temperature: {config['temperature']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_simple_autogen():
    """Test a simple AutoGen conversation."""
    print("\n🤖 Testing Simple AutoGen Conversation...")
    print("=" * 45)
    
    try:
        from models import create_sample_agents, GroqModelConfig
        from autogen import UserProxyAgent, AssistantAgent
        
        # Create configuration
        groq_config = GroqModelConfig()
        
        # Use the fastest model for testing
        model_name = "llama-3.1-8b-instant"
        config = groq_config.create_autogen_config(model_name)
        
        print(f"🚀 Creating agents with {model_name}...")
        
        # Create a simple assistant for testing
        assistant = AssistantAgent(
            name="test_assistant",
            llm_config=config,
            system_message="You are a helpful assistant. Keep responses brief. End with TERMINATE."
        )
        
        user_proxy = UserProxyAgent(
            name="test_user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )
        
        print("💬 Starting test conversation...")
        
        # Simple test message
        test_message = "Say hello and tell me you're working correctly. Keep it brief."
        
        # Start conversation
        user_proxy.initiate_chat(assistant, message=test_message)
        
        print("✅ AutoGen conversation completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install pyautogen groq")
        return False
    except Exception as e:
        print(f"❌ Conversation error: {e}")
        return False


def test_groq_direct():
    """Test direct Groq API call (without AutoGen)."""
    print("\n🔌 Testing Direct Groq API Call...")
    print("=" * 40)
    
    try:
        from groq import Groq
        
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        print("📡 Making API call to Groq...")
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say 'Hello from Groq!' and nothing else."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        message = response.choices[0].message.content
        print(f"📝 Response: {message}")
        print("✅ Direct Groq API call successful!")
        return True
        
    except Exception as e:
        print(f"❌ Direct API error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 AutoGen + Groq Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Groq Connection", test_groq_connection),
        ("Direct Groq API", test_groq_direct),
        ("AutoGen Integration", test_simple_autogen),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n🎯 Running: {test_name}")
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print(f"\n⚠️ Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test failed with unexpected error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Your setup is ready to go!")
        print("\n🚀 Next steps:")
        print("   - Run: python example.py")
        print("   - Explore the README.md for more examples")
        print("   - Try different models in models.py")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
        print("\n🔧 Common fixes:")
        print("   - Verify your GROQ_API_KEY is correct")
        print("   - Check your internet connection")
        print("   - Ensure all dependencies are installed")


if __name__ == "__main__":
    main()
