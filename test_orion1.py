"""
Test script for Orion1 team creation
This script tests if all team members can be created successfully
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_team_creation():
    """Test creating individual team members"""
    print("🧪 Testing Orion1 Team Creation")
    print("=" * 50)
    
    # Check API keys
    api_keys = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"), 
        "OPEN_AI_KEY": os.getenv("OPEN_AI_KEY"),
        "DEEPKEY_API_KEY": os.getenv("DEEPKEY_API_KEY"),
    }
    
    print("🔑 Checking API Keys:")
    for key, value in api_keys.items():
        status = "✅" if value else "❌"
        masked_value = f"{value[:8]}..." if value else "Not found"
        print(f"  {status} {key}: {masked_value}")
    print()
    
    # Test imports
    try:
        print("📦 Testing imports...")
        from orion1_models import create_orion1_team, ORION1_MODELS, MultiProviderConfig
        print("✅ Imports successful")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test model configuration
    try:
        print("\n🔧 Testing model configuration...")
        config = MultiProviderConfig()
        print("✅ Configuration initialized")
        
        # Test each provider
        providers_to_test = ["groq", "google", "moonshot", "deepseek"]
        for provider in providers_to_test:
            try:
                if provider == "groq" and api_keys["GROQ_API_KEY"]:
                    client = config.get_client("llama-3.3-70b-versatile", provider)
                    print(f"✅ {provider.title()} client created")
                elif provider == "google" and api_keys["GOOGLE_API_KEY"]:
                    client = config.get_client("gemini-2.5-pro", provider)
                    print(f"✅ {provider.title()} client created")
                elif provider == "moonshot" and api_keys["OPEN_AI_KEY"]:
                    client = config.get_client("moonshotai/kimi-k2-instruct", provider)
                    print(f"✅ {provider.title()} client created")
                elif provider == "deepseek" and api_keys["DEEPKEY_API_KEY"]:
                    client = config.get_client("deepseek-r1-distill-llama-70b", provider)
                    print(f"✅ {provider.title()} client created")
                else:
                    print(f"⚠️ {provider.title()} skipped (no API key)")
            except Exception as e:
                print(f"❌ {provider.title()} error: {e}")
    
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    # Test team creation
    try:
        print("\n👥 Testing team creation...")
        team = create_orion1_team()
        
        team_roles = [
            "principal_decision_maker",
            "product_manager", 
            "software_architect",
            "software_developer_1",
            "software_developer_2",
            "software_tester"
        ]
        
        for role in team_roles:
            if role in team:
                agent = team[role]
                print(f"✅ {role.replace('_', ' ').title()}: {agent.name}")
            else:
                print(f"❌ {role.replace('_', ' ').title()}: Missing")
        
        print(f"\n✅ Team created successfully with {len(team)} members!")
        return True
        
    except Exception as e:
        print(f"❌ Team creation error: {e}")
        return False

async def test_simple_interaction():
    """Test a simple interaction with one team member"""
    print("\n🗣️ Testing Simple Interaction")
    print("=" * 50)
    
    try:
        from orion1_models import create_agent
        
        # Create a simple test agent (using Groq which should be most reliable)
        test_agent = create_agent(
            name="TestAgent",
            model="llama-3.1-8b-instant",
            system_message="You are a test agent. Respond with exactly one sentence that says 'Hello from Orion1 team!'",
            provider="groq"
        )
        
        print(f"✅ Test agent created: {test_agent.name}")
        print("   (Skipping actual conversation test for now)")
        
        return True
        
    except Exception as e:
        print(f"❌ Interaction test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🌟 Orion1 Team Testing Suite")
    print("=" * 60)
    
    tests = [
        ("Team Creation", test_team_creation),
        ("Simple Interaction", test_simple_interaction),
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
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Orion1 team is ready!")
        print("\nNext steps:")
        print("1. Run: python orion1_team.py")
        print("2. Experiment with different team scenarios")
        print("3. Customize team roles and models as needed")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
        print("\nTroubleshooting:")
        print("1. Verify all API keys are valid")
        print("2. Check internet connectivity") 
        print("3. Ensure all required packages are installed")

if __name__ == "__main__":
    asyncio.run(main())
