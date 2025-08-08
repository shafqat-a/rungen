# 🌟 Orion1 Software Development Team

A complete AI-powered software development team using multiple state-of-the-art AI models from different providers.

## 👥 Team Structure

### 👑 Principal Decision Maker
- **Model**: `llama-3.3-70b-versatile` (Groq)
- **Role**: Strategic decisions, conflict resolution, project oversight
- **Responsibilities**:
  - Make final strategic and technical decisions
  - Resolve conflicts between team members
  - Ensure project alignment with business goals
  - Approve major architectural changes
  - Manage project timeline and priorities

### 📋 Product Manager
- **Model**: `llama-3.3-70b-versatile` (Groq)
- **Role**: Requirements, user stories, stakeholder communication
- **Responsibilities**:
  - Define product requirements and user stories
  - Prioritize features and backlog items
  - Communicate with stakeholders
  - Ensure user experience is optimal
  - Track project progress and deliverables

### 🏗️ Software Architect
- **Model**: `gemini-2.5-pro` (Google)
- **Role**: System design, technology decisions, technical documentation
- **Responsibilities**:
  - Design system architecture and technical solutions
  - Make technology stack decisions
  - Ensure scalability, security, and maintainability
  - Create technical documentation and diagrams
  - Review and approve architectural changes

### 👨‍💻 Software Developer 1
- **Model**: `moonshotai/kimi-k2-instruct` (Moonshot AI)
- **Role**: Feature implementation, code quality, collaboration
- **Responsibilities**:
  - Implement features according to specifications
  - Write clean, maintainable, and efficient code
  - Participate in code reviews
  - Debug and fix issues
  - Collaborate with other developers

### 👩‍💻 Software Developer 2
- **Model**: `moonshotai/kimi-k2-instruct` (Moonshot AI)
- **Role**: Feature implementation, performance optimization, UX
- **Responsibilities**:
  - Implement features according to specifications
  - Write clean, maintainable, and efficient code
  - Focus on performance optimization and user experience
  - Participate in code reviews
  - Debug and fix issues

### 🧪 Software Tester (Playwright Expert)
- **Model**: `deepseek-r1-distill-llama-70b` (DeepSeek)
- **Role**: Quality assurance, automated testing with Playwright
- **Responsibilities**:
  - Design and implement comprehensive test strategies
  - Write automated tests using Playwright for web applications
  - Perform manual testing when needed
  - Create test cases and documentation
  - Report bugs and verify fixes
  - Ensure quality standards are met

## 🚀 Quick Start

### Prerequisites
1. Python 3.8+ with virtual environment
2. API keys for:
   - Groq (`GROQ_API_KEY`)
   - Google AI (`GOOGLE_API_KEY`)
   - OpenAI/Moonshot (`OPEN_AI_KEY`)
   - DeepSeek (`DEEPKEY_API_KEY`)

### Setup
```bash
# Activate virtual environment
source rungen/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test team creation
python test_orion1.py

# Run team demonstration
python orion1_team.py
```

## 📋 Usage Examples

### 1. Team Meeting
```python
from orion1_models import create_orion1_team
import asyncio

async def team_meeting():
    team = create_orion1_team()
    
    # Your meeting topic
    topic = "Weekly Sprint Planning and Risk Assessment"
    
    # Run team discussion
    await run_team_meeting(topic, team)

asyncio.run(team_meeting())
```

### 2. Project Planning
```python
async def project_planning():
    team = create_orion1_team()
    
    project = "E-commerce Platform with Real-time Analytics"
    await run_project_planning(project, team)
```

### 3. Code Review
```python
async def code_review():
    team = create_orion1_team()
    
    code = """
    async function processPayment(paymentData) {
        // Your code here
    }
    """
    
    await run_code_review_session(code, team)
```

## 🔧 Configuration

### Supported Providers
- **Groq**: Fast inference with Llama models
- **Google**: Advanced reasoning with Gemini models
- **Moonshot AI**: Specialized coding capabilities
- **DeepSeek**: Strong testing and analysis skills
- **OpenAI**: General-purpose capabilities

### Model Configuration
Edit `orion1_models.py` to customize:
- Team member models
- System messages/roles
- Provider settings

### Environment Variables
```bash
# Required API Keys
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key  
OPEN_AI_KEY=your_openai_key
DEEPKEY_API_KEY=your_deepseek_key

# Optional settings
DEFAULT_GROQ_MODEL=llama-3.3-70b-versatile
AUTOGEN_WORKSPACE=workspace
```

## 🎯 Team Scenarios

The Orion1 team can handle various software development scenarios:

1. **Sprint Planning**: Weekly planning and risk assessment
2. **Project Kickoff**: New project planning and architecture
3. **Code Reviews**: Multi-perspective code analysis
4. **Bug Triage**: Issue analysis and resolution planning
5. **Technical Discussions**: Architecture and design decisions
6. **Testing Strategy**: Comprehensive QA planning with Playwright

## 🛠️ Customization

### Adding New Team Members
```python
# In orion1_models.py
new_member = create_agent(
    name="Your_Role",
    model="your_preferred_model",
    system_message="Your role description...",
    provider="your_provider"
)
```

### Changing Models
Update the `ORION1_MODELS` dictionary in `orion1_models.py`:
```python
ORION1_MODELS = {
    "principal_decision_maker": "your_preferred_model",
    # ... other roles
}
```

### Custom Workflows
Create new functions in `orion1_team.py` for specific workflows:
```python
async def custom_workflow(task, team):
    # Your custom team interaction logic
    pass
```

## 📊 Performance Notes

- **Groq models**: Fastest inference, good for decision-making
- **Gemini models**: Best for complex reasoning and architecture
- **Moonshot models**: Excellent for coding tasks
- **DeepSeek models**: Strong analytical capabilities for testing

## 🔍 Troubleshooting

### Common Issues
1. **API Key Errors**: Verify all keys in `.env` file
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Model Timeouts**: Some models may be slower than others
4. **Rate Limits**: Each provider has different rate limits

### Testing
```bash
# Test individual components
python test_orion1.py

# Test specific providers
python -c "from orion1_models import MultiProviderConfig; config = MultiProviderConfig(); print('✅ Config OK')"
```

## 🎉 Success Indicators

When everything is working correctly:
- ✅ All API keys validated
- ✅ Team members created successfully  
- ✅ Multi-provider model access
- ✅ Conversation flows working
- ✅ Role-based responses from each agent

The Orion1 team is now ready for real software development projects! 🚀
