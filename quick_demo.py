"""
Quick Orion1 Team Demo
Shows team initialization and basic info without full conversation
"""

import asyncio
import os
from dotenv import load_dotenv
from orion1_models import create_orion1_team, ORION1_MODELS

# Load environment variables
load_dotenv()

async def quick_demo():
    """Quick demonstration of Orion1 team"""
    print("🌟 Orion1 Software Development Team - Quick Demo")
    print("=" * 60)
    
    # Check API keys
    required_keys = ["GROQ_API_KEY", "GOOGLE_API_KEY", "OPEN_AI_KEY", "DEEPKEY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        return
    
    print("✅ All API keys found!")
    print()
    
    # Show team structure
    print("👥 Team Structure:")
    team_info = {
        "👑 Principal Decision Maker": {
            "model": ORION1_MODELS["principal_decision_maker"],
            "provider": "Groq (llama-3.3-70b-versatile)",
            "focus": "Strategic decisions & project oversight"
        },
        "📋 Product Manager": {
            "model": ORION1_MODELS["product_manager"],
            "provider": "Groq (llama-3.3-70b-versatile)",
            "focus": "Requirements & stakeholder communication"
        },
        "🏗️ Software Architect": {
            "model": ORION1_MODELS["software_architect"],
            "provider": "Google (gemini-2.5-pro)",
            "focus": "System design & technical architecture"
        },
        "👨‍💻 Software Developer 1": {
            "model": ORION1_MODELS["software_developer"],
            "provider": "Moonshot AI (kimi-k2-instruct)",
            "focus": "Feature implementation & code quality"
        },
        "👩‍💻 Software Developer 2": {
            "model": ORION1_MODELS["software_developer"],
            "provider": "Moonshot AI (kimi-k2-instruct)",
            "focus": "Performance optimization & UX"
        },
        "🧪 Software Tester": {
            "model": ORION1_MODELS["software_tester"],
            "provider": "DeepSeek (r1-distill-llama-70b)",
            "focus": "Playwright testing & quality assurance"
        }
    }
    
    for role, info in team_info.items():
        print(f"{role}")
        print(f"   Provider: {info['provider']}")
        print(f"   Focus: {info['focus']}")
        print()
    
    # Create team
    print("🔧 Initializing team...")
    try:
        team = create_orion1_team()
        print("✅ Team created successfully!")
        print(f"   Team size: {len(team)} members")
        
        # Show team members
        print("\n📋 Active Team Members:")
        for role, agent in team.items():
            role_display = role.replace('_', ' ').title()
            print(f"   ✅ {role_display}: {agent.name}")
        
        print("\n🚀 Team Capabilities:")
        capabilities = [
            "Sprint planning and project management",
            "Technical architecture and system design", 
            "Feature development and implementation",
            "Code review and quality assurance",
            "Automated testing with Playwright",
            "Bug analysis and resolution planning",
            "Performance optimization strategies",
            "User experience and product requirements"
        ]
        
        for capability in capabilities:
            print(f"   • {capability}")
        
        print("\n🎯 Ready for:")
        scenarios = [
            "Team meetings and sprint planning",
            "Project planning for new initiatives", 
            "Code review sessions",
            "Architecture and design discussions",
            "Testing strategy development",
            "Bug triage and resolution planning"
        ]
        
        for scenario in scenarios:
            print(f"   • {scenario}")
        
        print("\n💡 To run full team scenarios:")
        print("   python orion1_team.py")
        
        print("\n✨ Orion1 team is ready for action! ✨")
        
    except Exception as e:
        print(f"❌ Error creating team: {e}")

if __name__ == "__main__":
    asyncio.run(quick_demo())
