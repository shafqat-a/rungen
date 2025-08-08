"""
Orion1 Software Development Team - Project Oriented
Interactive team that asks for objectives and provides file/command tools
"""

import asyncio
import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv
from dataclasses import dataclass

# AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_core.tools import Tool, ToolSchema

# Multi-provider support
from orion1_models import create_orion1_team, ORION1_MODELS

# Load environment variables
load_dotenv()

# ============================================================================
# TOOL DEFINITIONS FOR FILE OPERATIONS AND COMMAND EXECUTION
# ============================================================================

@dataclass
class FileReadResult:
    """Result of reading a file"""
    success: bool
    content: str = ""
    error: str = ""

@dataclass 
class FileWriteResult:
    """Result of writing a file"""
    success: bool
    message: str = ""
    error: str = ""

@dataclass
class CommandResult:
    """Result of executing a command"""
    success: bool
    stdout: str = ""
    stderr: str = ""
    return_code: int = 0
    command: str = ""

class ProjectTools:
    """Tools for file operations and command execution"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.workspace_dir = self.project_root / "workspace"
        self.workspace_dir.mkdir(exist_ok=True)
        
    def read_file(self, file_path: str) -> FileReadResult:
        """
        Read contents of a file
        
        Args:
            file_path: Path to the file to read (relative to project root)
            
        Returns:
            FileReadResult with content or error
        """
        try:
            full_path = self.project_root / file_path
            
            # Security check - ensure we're not reading outside project
            if not str(full_path.resolve()).startswith(str(self.project_root)):
                return FileReadResult(
                    success=False,
                    error=f"Access denied: Path outside project root: {file_path}"
                )
            
            if not full_path.exists():
                return FileReadResult(
                    success=False,
                    error=f"File not found: {file_path}"
                )
                
            content = full_path.read_text(encoding='utf-8')
            return FileReadResult(
                success=True,
                content=content
            )
            
        except Exception as e:
            return FileReadResult(
                success=False,
                error=f"Error reading file {file_path}: {str(e)}"
            )
    
    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> FileWriteResult:
        """
        Write content to a file
        
        Args:
            file_path: Path to the file to write (relative to project root)
            content: Content to write
            create_dirs: Whether to create parent directories if they don't exist
            
        Returns:
            FileWriteResult with success status
        """
        try:
            full_path = self.project_root / file_path
            
            # Security check - ensure we're not writing outside project
            if not str(full_path.resolve()).startswith(str(self.project_root)):
                return FileWriteResult(
                    success=False,
                    error=f"Access denied: Path outside project root: {file_path}"
                )
            
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)
            
            full_path.write_text(content, encoding='utf-8')
            return FileWriteResult(
                success=True,
                message=f"Successfully wrote {len(content)} characters to {file_path}"
            )
            
        except Exception as e:
            return FileWriteResult(
                success=False,
                error=f"Error writing file {file_path}: {str(e)}"
            )
    
    def list_files(self, directory: str = ".", pattern: str = "*", recursive: bool = True) -> Dict[str, Any]:
        """
        List files in a directory
        
        Args:
            directory: Directory to list (relative to project root)
            pattern: Glob pattern to match files
            recursive: Whether to search recursively
            
        Returns:
            Dictionary with file listing or error
        """
        try:
            full_path = self.project_root / directory
            
            # Security check
            if not str(full_path.resolve()).startswith(str(self.project_root)):
                return {
                    "success": False,
                    "error": f"Access denied: Path outside project root: {directory}"
                }
            
            if not full_path.exists():
                return {
                    "success": False,
                    "error": f"Directory not found: {directory}"
                }
            
            if recursive:
                files = list(full_path.rglob(pattern))
            else:
                files = list(full_path.glob(pattern))
            
            file_list = []
            for f in files:
                rel_path = f.relative_to(self.project_root)
                file_info = {
                    "path": str(rel_path),
                    "name": f.name,
                    "is_file": f.is_file(),
                    "is_dir": f.is_dir(),
                    "size": f.stat().st_size if f.is_file() else 0
                }
                file_list.append(file_info)
            
            return {
                "success": True,
                "directory": directory,
                "pattern": pattern,
                "recursive": recursive,
                "files": file_list,
                "count": len(file_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error listing files in {directory}: {str(e)}"
            }
    
    def run_command(self, command: str, cwd: Optional[str] = None, timeout: int = 30) -> CommandResult:
        """
        Execute a shell command
        
        Args:
            command: Command to execute
            cwd: Working directory (relative to project root)
            timeout: Command timeout in seconds
            
        Returns:
            CommandResult with output and status
        """
        try:
            # Set working directory
            if cwd:
                work_dir = self.project_root / cwd
                if not str(work_dir.resolve()).startswith(str(self.project_root)):
                    return CommandResult(
                        success=False,
                        stderr=f"Access denied: Working directory outside project root: {cwd}",
                        return_code=-1,
                        command=command
                    )
            else:
                work_dir = self.project_root
            
            # Security: Basic command filtering
            dangerous_commands = ['rm -rf', 'format', 'del /f', 'sudo rm', 'chmod 777']
            if any(dangerous in command.lower() for dangerous in dangerous_commands):
                return CommandResult(
                    success=False,
                    stderr=f"Potentially dangerous command blocked: {command}",
                    return_code=-1,
                    command=command
                )
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return CommandResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                command=command
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stderr=f"Command timed out after {timeout} seconds",
                return_code=-1,
                command=command
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stderr=f"Error executing command: {str(e)}",
                return_code=-1,
                command=command
            )

# ============================================================================
# TOOL WRAPPERS FOR AUTOGEN
# ============================================================================

def create_file_tools(project_tools: ProjectTools) -> List[Tool]:
    """Create AutoGen tool wrappers for file operations"""
    
    tools = []
    
    # Read file tool
    @Tool
    def read_file(file_path: str) -> str:
        """
        Read the contents of a file
        
        Args:
            file_path: Path to the file to read (relative to project root)
            
        Returns:
            File contents or error message
        """
        result = project_tools.read_file(file_path)
        if result.success:
            return f"File: {file_path}\n\n{result.content}"
        else:
            return f"❌ Error reading {file_path}: {result.error}"
    
    # Write file tool
    @Tool
    def write_file(file_path: str, content: str) -> str:
        """
        Write content to a file
        
        Args:
            file_path: Path to the file to write (relative to project root)
            content: Content to write to the file
            
        Returns:
            Success message or error
        """
        result = project_tools.write_file(file_path, content)
        if result.success:
            return f"✅ {result.message}"
        else:
            return f"❌ Error writing {file_path}: {result.error}"
    
    # List files tool
    @Tool
    def list_files(directory: str = ".", pattern: str = "*", recursive: bool = True) -> str:
        """
        List files in a directory
        
        Args:
            directory: Directory to list (default: current directory)
            pattern: Glob pattern to match files (default: all files)
            recursive: Whether to search recursively (default: True)
            
        Returns:
            Formatted file listing
        """
        result = project_tools.list_files(directory, pattern, recursive)
        if result["success"]:
            files = result["files"]
            output = f"📁 Directory: {result['directory']}\n"
            output += f"🔍 Pattern: {result['pattern']}\n"
            output += f"📊 Found {result['count']} items\n\n"
            
            for file_info in files[:20]:  # Limit to first 20 items
                icon = "📄" if file_info["is_file"] else "📁"
                size = f" ({file_info['size']} bytes)" if file_info["is_file"] else ""
                output += f"{icon} {file_info['path']}{size}\n"
            
            if len(files) > 20:
                output += f"... and {len(files) - 20} more items\n"
                
            return output
        else:
            return f"❌ Error listing files: {result['error']}"
    
    # Run command tool
    @Tool 
    def run_command(command: str, cwd: str = ".", timeout: int = 30) -> str:
        """
        Execute a shell command
        
        Args:
            command: Command to execute
            cwd: Working directory (default: project root)
            timeout: Command timeout in seconds (default: 30)
            
        Returns:
            Command output and status
        """
        result = project_tools.run_command(command, cwd, timeout)
        
        output = f"💻 Command: {result.command}\n"
        output += f"📍 Directory: {cwd}\n"
        output += f"✅ Success: {result.success}\n"
        output += f"🔢 Return code: {result.return_code}\n\n"
        
        if result.stdout:
            output += f"📤 STDOUT:\n{result.stdout}\n\n"
        
        if result.stderr:
            output += f"📥 STDERR:\n{result.stderr}\n\n"
            
        return output
    
    tools.extend([read_file, write_file, list_files, run_command])
    return tools

# ============================================================================
# ENHANCED ORION1 TEAM WITH TOOLS
# ============================================================================

class Orion1ProjectTeam:
    """Enhanced Orion1 team with project management capabilities"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.project_tools = ProjectTools(project_root)
        self.tools = create_file_tools(self.project_tools)
        self.team_members = {}
        self.objective = ""
        
    def check_api_keys(self) -> List[str]:
        """Check which API keys are available"""
        required_keys = {
            "GROQ_API_KEY": "Groq (Principal Decision Maker, Product Manager)",
            "GOOGLE_API_KEY": "Google Gemini (Software Architect)", 
            "OPEN_AI_KEY": "Moonshot AI (Software Developers)",
            "DEEPKEY_API_KEY": "DeepSeek (Software Tester)"
        }
        
        missing_keys = []
        available_keys = []
        
        for key, description in required_keys.items():
            if os.getenv(key):
                available_keys.append(f"✅ {description}")
            else:
                missing_keys.append(f"❌ {description} - Missing {key}")
        
        return missing_keys, available_keys
    
    def create_enhanced_team(self) -> Dict[str, AssistantAgent]:
        """Create the Orion1 team with tool access"""
        # Get base team
        base_team = create_orion1_team()
        
        # Add tools to each team member
        enhanced_team = {}
        
        for role, agent in base_team.items():
            # Create enhanced agent with tools
            enhanced_agent = AssistantAgent(
                name=agent.name,
                description=agent.description,
                system_message=self._get_enhanced_system_message(role, agent.system_message),
                model_client=agent.model_client,
                tools=self.tools  # Add tools to each agent
            )
            enhanced_team[role] = enhanced_agent
        
        return enhanced_team
    
    def _get_enhanced_system_message(self, role: str, base_message: str) -> str:
        """Enhance system message with tool usage instructions"""
        tool_instructions = """

AVAILABLE TOOLS:
You have access to the following tools for project work:

1. read_file(file_path) - Read contents of any file in the project
2. write_file(file_path, content) - Create or modify files
3. list_files(directory, pattern, recursive) - Browse project structure
4. run_command(command, cwd, timeout) - Execute shell commands

TOOL USAGE GUIDELINES:
- Always use tools when you need to examine or modify files
- Use list_files() to understand project structure before making changes
- Use read_file() to examine existing code before modifying
- Use write_file() to create new files or update existing ones
- Use run_command() to run tests, build commands, or other shell operations
- Always verify your changes by reading files back after writing
- Be methodical and explain what you're doing with each tool

SECURITY NOTES:
- All file operations are restricted to the project directory
- Dangerous commands are automatically blocked
- Always use relative paths from the project root

"""
        
        role_specific_instructions = {
            "principal_decision_maker": """
As Principal Decision Maker, use tools to:
- Review overall project structure and progress
- Examine key configuration files and documentation
- Make strategic decisions based on actual project state
""",
            "product_manager": """
As Product Manager, use tools to:
- Review requirements documents and user stories
- Check project documentation for completeness
- Verify that features align with requirements
- Create and update project specifications
""",
            "software_architect": """
As Software Architect, use tools to:
- Examine codebase structure and architecture
- Review design documents and technical specifications
- Create architectural diagrams and documentation
- Analyze code quality and technical debt
""",
            "software_developer_1": """
As Software Developer, use tools to:
- Examine existing code before making changes
- Implement new features and fix bugs
- Write and run unit tests
- Create technical documentation for your code
""",
            "software_developer_2": """
As Software Developer, use tools to:
- Review code for performance optimization opportunities
- Implement features with focus on user experience
- Run performance tests and benchmarks
- Optimize existing code for better performance
""",
            "software_tester": """
As Software Tester with Playwright expertise, use tools to:
- Examine test files and test coverage
- Create comprehensive test suites using Playwright
- Run automated tests and analyze results
- Create test documentation and bug reports
- Set up CI/CD testing pipelines
"""
        }
        
        enhanced_message = base_message + tool_instructions
        if role in role_specific_instructions:
            enhanced_message += role_specific_instructions[role]
            
        return enhanced_message
    
    async def get_user_objective(self) -> str:
        """Get project objective from user"""
        print("🎯 Welcome to Orion1 - AI Software Development Team")
        print("=" * 60)
        print()
        print("I'm ready to help you with your software development project!")
        print("Please provide your project objective or describe what you'd like to build.")
        print()
        print("Examples:")
        print("• Build a REST API for task management")
        print("• Create a React dashboard for analytics")
        print("• Develop a Python CLI tool for data processing")
        print("• Set up automated testing for existing codebase")
        print()
        
        while True:
            objective = input("📝 Project Objective: ").strip()
            if objective:
                self.objective = objective
                return objective
            print("❌ Please provide a project objective.")
    
    async def analyze_project_context(self) -> str:
        """Analyze current project context"""
        print("\n🔍 Analyzing current project context...")
        
        context = []
        
        # Check project structure
        files_result = self.project_tools.list_files(".", "*", True)
        if files_result["success"]:
            context.append(f"📁 Project contains {files_result['count']} files")
            
            # Check for key files
            key_files = ["README.md", "package.json", "requirements.txt", "Cargo.toml", "pom.xml"]
            found_files = []
            for file_info in files_result["files"]:
                if file_info["name"] in key_files:
                    found_files.append(file_info["name"])
            
            if found_files:
                context.append(f"📄 Found key files: {', '.join(found_files)}")
        
        # Check if it's a git repository
        git_result = self.project_tools.run_command("git status", ".", 5)
        if git_result.success:
            context.append("📦 Git repository detected")
        
        # Check for common project types
        project_types = []
        file_patterns = {
            "Python": ["*.py", "requirements.txt", "setup.py"],
            "JavaScript/Node.js": ["package.json", "*.js", "*.ts"],
            "React": ["package.json", "public/index.html", "src/App.js"],
            "Java": ["*.java", "pom.xml", "build.gradle"],
            "Rust": ["Cargo.toml", "*.rs"],
            "Go": ["go.mod", "*.go"]
        }
        
        for proj_type, patterns in file_patterns.items():
            found = any(
                any(pattern in f["name"] or f["path"].endswith(pattern.replace("*", "")) 
                    for f in files_result.get("files", []))
                for pattern in patterns
            )
            if found:
                project_types.append(proj_type)
        
        if project_types:
            context.append(f"🛠️ Detected project types: {', '.join(project_types)}")
        
        return "\n".join(context) if context else "📂 Empty or new project directory"
    
    async def run_project_session(self):
        """Main project session with user interaction"""
        
        # Check API keys
        missing_keys, available_keys = self.check_api_keys()
        
        if missing_keys:
            print("⚠️ Missing API Keys:")
            for key in missing_keys:
                print(f"  {key}")
            print("\nAvailable services:")
            for key in available_keys:
                print(f"  {key}")
            print()
            
            proceed = input("Continue with available services? (y/n): ").lower()
            if proceed != 'y':
                print("Please configure your API keys and try again.")
                return
        
        # Get user objective
        objective = await self.get_user_objective()
        
        # Analyze project context
        context = await self.analyze_project_context()
        
        print(f"\n📋 Project Context:")
        print(context)
        print()
        
        # Confirm with user
        print(f"🎯 Objective: {objective}")
        print()
        confirm = input("Proceed with this objective? (y/n): ").lower()
        if confirm != 'y':
            print("Session cancelled.")
            return
        
        # Create enhanced team
        print("\n🚀 Initializing Orion1 team with project tools...")
        try:
            team_members = self.create_enhanced_team()
            print("✅ Team created successfully!")
            
            # Show team composition
            print("\n👥 Team Members:")
            for role, agent in team_members.items():
                print(f"  • {agent.name}")
            print()
            
            # Create the project planning prompt
            planning_prompt = f"""
PROJECT KICKOFF SESSION

OBJECTIVE: {objective}

CURRENT PROJECT CONTEXT:
{context}

TEAM INSTRUCTIONS:
Each team member should contribute from their expertise using the available tools:

PRINCIPAL DECISION MAKER:
- Use list_files() to understand current project structure
- Analyze the objective and set strategic direction
- Define project scope, priorities, and success criteria
- Identify key risks and mitigation strategies

PRODUCT MANAGER:
- Use read_file() to examine any existing requirements or documentation
- Break down the objective into specific user stories and features
- Define acceptance criteria for each feature
- Prioritize features for MVP and future releases

SOFTWARE ARCHITECT:
- Use list_files() and read_file() to examine existing codebase
- Design technical architecture for the objective
- Choose appropriate technology stack and frameworks
- Create high-level system design and component architecture

SOFTWARE DEVELOPER 1:
- Use read_file() to examine existing code structure
- Estimate development effort for each component
- Identify implementation challenges and solutions
- Plan development approach and coding standards

SOFTWARE DEVELOPER 2:
- Use list_files() to understand current project organization
- Focus on performance implications and optimization strategies
- Consider user experience and interface design
- Identify potential bottlenecks and scalability concerns

SOFTWARE TESTER (Playwright Expert):
- Use read_file() to examine any existing test files
- Design comprehensive testing strategy using Playwright
- Define test scenarios, edge cases, and automation approach
- Plan testing timeline and quality assurance process

IMPORTANT:
- Use the available tools (read_file, write_file, list_files, run_command) to examine the project
- Be specific and actionable in your recommendations
- Create concrete deliverables like file specifications, architecture diagrams, test plans
- Consider the current project state when making suggestions
- Focus on practical, implementable solutions

Let's begin the project planning session!
"""
            
            # Create team chat
            team_list = list(team_members.values())
            team_chat = RoundRobinGroupChat(team_list)
            
            print("🗣️ Starting project planning session...")
            print("=" * 60)
            
            # Run the planning session
            result = await Console(team_chat.run_stream(task=planning_prompt))
            
            print("\n" + "=" * 60)
            print("✅ Project planning session completed!")
            print("\n💡 The team is ready to start development work!")
            print("\nNext steps:")
            print("• Review the team's recommendations")
            print("• Execute specific development tasks")
            print("• Use the team for ongoing project collaboration")
            
        except Exception as e:
            print(f"❌ Error during team session: {e}")
            print("\nTroubleshooting:")
            print("1. Check all API keys are valid")
            print("2. Ensure internet connectivity")
            print("3. Verify all required packages are installed")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

async def main():
    """Main function for project-oriented Orion1 team"""
    
    # Setup project directory
    project_root = os.getcwd()
    print(f"🏠 Project root: {project_root}")
    
    # Create team instance
    orion1_team = Orion1ProjectTeam(project_root)
    
    # Run interactive session
    await orion1_team.run_project_session()

if __name__ == "__main__":
    print("🌟 Orion1 Project-Oriented Team")
    print("🛠️ With File Operations and Command Execution")
    print()
    
    asyncio.run(main())
