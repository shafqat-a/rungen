"""
Orion1 Software Development Team
A complete AI-powered software development team using different AI models
"""

import asyncio
import os
from dotenv import load_dotenv
from orion1_models import create_orion1_team, ORION1_MODELS
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def team_introduction():
    """Introduce the Orion1 team members"""
    print("🚀 Orion1 Software Development Team")
    print("=" * 60)
    print()
    
    team_structure = {
        "👑 Principal Decision Maker": {
            "model": ORION1_MODELS["principal_decision_maker"],
            "provider": "Groq",
            "role": "Strategic decisions, conflict resolution, project oversight"
        },
        "📋 Product Manager": {
            "model": ORION1_MODELS["product_manager"], 
            "provider": "Groq",
            "role": "Requirements, user stories, stakeholder communication"
        },
        "🏗️ Software Architect": {
            "model": ORION1_MODELS["software_architect"],
            "provider": "Google Gemini",
            "role": "System design, technology decisions, technical documentation"
        },
        "👨‍💻 Software Developer 1": {
            "model": ORION1_MODELS["software_developer"],
            "provider": "Moonshot AI",
            "role": "Feature implementation, code quality, collaboration"
        },
        "👩‍💻 Software Developer 2": {
            "model": ORION1_MODELS["software_developer"],
            "provider": "Moonshot AI", 
            "role": "Feature implementation, performance optimization, UX"
        },
        "🧪 Software Tester": {
            "model": ORION1_MODELS["software_tester"],
            "provider": "DeepSeek",
            "role": "Playwright testing, quality assurance, bug reporting"
        }
    }
    
    for role, info in team_structure.items():
        print(f"{role}")
        print(f"   Model: {info['model']} ({info['provider']})")
        print(f"   Role: {info['role']}")
        print()

async def run_team_meeting(topic, team):
    """Run a team meeting on a specific topic"""
    print(f"📅 Team Meeting: {topic}")
    print("=" * 60)
    
    # Create team chat with all members
    team_members = list(team.values())
    team_chat = RoundRobinGroupChat(team_members)
    
    # Meeting prompt
    meeting_prompt = f"""
    Team Meeting Topic: {topic}
    
    Each team member should contribute from their expertise:
    - Principal Decision Maker: Provide strategic direction and decisions
    - Product Manager: Focus on user requirements and business value
    - Software Architect: Discuss technical architecture and design
    - Software Developer 1 & 2: Share implementation insights and concerns
    - Software Tester: Address quality assurance and testing strategies
    
    Keep responses concise and focused. End with your key takeaway or recommendation.
    """
    
    print("🗣️ Starting team discussion...")
    print("-" * 40)
    
    result = await Console(team_chat.run_stream(task=meeting_prompt))
    
    print("\n✅ Meeting completed!")
    return result

async def run_project_planning(project_description, team):
    """Run project planning session"""
    print(f"📋 Project Planning Session")
    print("=" * 60)
    print(f"Project: {project_description}")
    print()
    
    planning_prompt = f"""
    Project Planning Session
    
    Project Description: {project_description}
    
    Each team member should contribute:
    
    Principal Decision Maker:
    - Define project scope and priorities
    - Set timeline expectations
    - Identify key risks and mitigation strategies
    
    Product Manager:
    - Define user stories and acceptance criteria
    - Prioritize features for MVP
    - Identify stakeholder requirements
    
    Software Architect:
    - Propose technical architecture
    - Recommend technology stack
    - Identify technical challenges and solutions
    
    Software Developer 1:
    - Estimate development effort
    - Identify implementation challenges
    - Suggest development approach
    
    Software Developer 2:
    - Review architecture for performance implications
    - Suggest optimization strategies
    - Identify potential bottlenecks
    
    Software Tester:
    - Define testing strategy using Playwright
    - Identify test scenarios and edge cases
    - Estimate testing effort and timeline
    
    Provide specific, actionable insights for this project.
    """
    
    team_members = list(team.values())
    team_chat = RoundRobinGroupChat(team_members)
    
    print("🚀 Starting project planning...")
    print("-" * 40)
    
    result = await Console(team_chat.run_stream(task=planning_prompt))
    
    print("\n✅ Project planning completed!")
    return result

async def run_code_review_session(code_snippet, team):
    """Run a code review session"""
    print(f"🔍 Code Review Session")
    print("=" * 60)
    
    review_prompt = f"""
    Code Review Session
    
    Code to Review:
    ```
    {code_snippet}
    ```
    
    Each team member should provide feedback:
    
    Principal Decision Maker:
    - Assess if code aligns with project goals
    - Identify any strategic concerns
    
    Product Manager:
    - Review from user experience perspective
    - Check if requirements are met
    
    Software Architect:
    - Review architectural compliance
    - Check design patterns and structure
    
    Software Developer 1:
    - Review code quality and best practices
    - Suggest improvements
    
    Software Developer 2:
    - Review for performance and optimization
    - Check error handling
    
    Software Tester:
    - Identify testing requirements
    - Suggest Playwright test scenarios
    - Point out potential edge cases
    
    Provide constructive feedback and specific suggestions.
    """
    
    team_members = list(team.values())
    team_chat = RoundRobinGroupChat(team_members)
    
    print("👀 Starting code review...")
    print("-" * 40)
    
    result = await Console(team_chat.run_stream(task=review_prompt))
    
    print("\n✅ Code review completed!")
    return result

async def main():
    """Main function to demonstrate Orion1 team capabilities"""
    
    # Check API keys
    required_keys = ["GROQ_API_KEY", "GOOGLE_API_KEY", "OPEN_AI_KEY", "DEEPKEY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("Please check your .env file")
        return
    
    print("🎯 Orion1 Team Demonstration")
    print("=" * 60)
    
    try:
        # Show team introduction
        await team_introduction()
        
        # Create the team
        print("🔧 Initializing Orion1 team...")
        team = create_orion1_team()
        print("✅ Team created successfully!")
        print()
        
        # Example scenarios
        scenarios = [
            {
                "type": "meeting",
                "topic": "Weekly Sprint Planning and Risk Assessment",
                "function": run_team_meeting
            },
            {
                "type": "planning", 
                "topic": "E-commerce Platform with Real-time Analytics",
                "function": run_project_planning
            },
            {
                "type": "code_review",
                "topic": """
async function processPayment(paymentData) {
    const { amount, cardNumber, cvv, expiryDate } = paymentData;
    
    if (!amount || amount <= 0) {
        throw new Error('Invalid amount');
    }
    
    const processedCard = cardNumber.replace(/\s/g, '');
    
    const paymentResult = await paymentGateway.charge({
        amount: amount,
        card: processedCard,
        cvv: cvv,
        expiry: expiryDate
    });
    
    return paymentResult;
}
                """,
                "function": run_code_review_session
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'='*60}")
            print(f"Scenario {i}: {scenario['type'].title()}")
            print(f"{'='*60}")
            
            try:
                if scenario["type"] == "code_review":
                    await scenario["function"](scenario["topic"], team)
                else:
                    await scenario["function"](scenario["topic"], team)
                    
                print(f"\n✅ Scenario {i} completed!")
                
                if i < len(scenarios):
                    print("\n⏱️ Waiting 3 seconds before next scenario...")
                    await asyncio.sleep(3)
                    
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
                continue
        
        print("\n🎉 Orion1 team demonstration completed!")
        print("\n💡 The team is ready for real projects!")
        
    except Exception as e:
        print(f"❌ Error initializing team: {e}")
        print("\nTroubleshooting:")
        print("1. Check all API keys are valid")
        print("2. Ensure internet connectivity")
        print("3. Verify all required packages are installed")

if __name__ == "__main__":
    print("🌟 Welcome to Orion1 - AI Software Development Team")
    asyncio.run(main())
