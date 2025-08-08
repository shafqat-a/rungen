"""
Simple working AutoGen + Groq example
This script demonstrates a basic conversation with AutoGen using Groq models.
"""

import asyncio
import os
from dotenv import load_dotenv
from models import create_assistant_agent, GROQ_MODELS
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def simple_groq_chat():
    """Simple chat example with Groq model"""
    print("🚀 AutoGen + Groq Simple Chat Example")
    print("=" * 50)
    
    try:
        # Check API key
        if not os.getenv("GROQ_API_KEY"):
            print("❌ GROQ_API_KEY not found in environment variables")
            return
        
        print("📋 Available Groq models:")
        for model, description in GROQ_MODELS.items():
            print(f"  • {model}: {description}")
        print()
        
        # Create assistant with Groq model
        assistant = create_assistant_agent(
            name="GroqAssistant",
            model="llama-3.1-8b-instant",  # Fast model
            system_message="You are a helpful AI assistant. Keep responses concise and helpful. Always end your response with 'DONE' when you've fully answered the question."
        )
        
        print(f"✅ Created assistant: {assistant.name}")
        print(f"📝 Model: llama-3.1-8b-instant")
        print()
        
        # Create team
        team = RoundRobinGroupChat([assistant])
        
        # Test questions
        questions = [
            "What is Python? Give me a brief explanation.",
            "List 3 benefits of using AutoGen for multi-agent systems.",
            "What makes Groq models fast?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"🤔 Question {i}: {question}")
            print("-" * 50)
            
            # Ask the question
            result = await Console(
                team.run_stream(task=question)
            )
            
            print(f"✅ Question {i} completed!")
            print("=" * 50)
            
            if i < len(questions):
                print("⏱️  Waiting 2 seconds before next question...")
                await asyncio.sleep(2)
        
        print("🎉 All questions completed successfully!")
        print("\n💡 Your AutoGen + Groq setup is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your GROQ_API_KEY in the .env file")
        print("2. Ensure you have internet connectivity")
        print("3. Verify your Groq API key is valid")

if __name__ == "__main__":
    print("🔧 Testing AutoGen with Groq Models")
    print("🌟 This is a simple working example")
    print()
    
    asyncio.run(simple_groq_chat())
