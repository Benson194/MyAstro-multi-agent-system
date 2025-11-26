"""
Main Entry Point for MyYear.AI
KEY CONCEPTS:
- Session management with InMemorySessionService
- State persistence across interactions
- Main workflows for wrapped generation and interactive chat
"""
import asyncio
import os
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, will use system env vars

from google.adk.runners import InMemoryRunner
from google.genai import types
from my_agent.agents.coordinator_agent import personal_curator


# KEY CONCEPT: Runner for executing agents
# The Runner manages agent execution, sessions, and event streaming
runner = InMemoryRunner(agent=personal_curator)


async def create_wrapped(csv_path: str, user_id: str = "user_001"):
    """
    Creates a personalized viewing wrapped experience.
    
    KEY CONCEPT: Session-based interaction
    
    Args:
        csv_path: Path to the viewing history CSV file
        user_id: User identifier for session management
    """
    print("🎬 Welcome to MyYear.AI - Your Personalized Viewing Wrapped!")
    print("=" * 70)
    print()
    
    # Create session for this user
    session_id = f"wrapped_{user_id}"
    
    # Prompt for wrapped generation
    prompt = f"""
    Please create my personalized viewing wrapped from this file: {csv_path}
    
    I want:
    1. Analysis of my viewing patterns and habits
    2. My viewing personality type
    3. A narrative story of my year in watching
    4. Evolution of my viewing over time
    5. Three shareable social media posts
    
    Make it fun, personal, and surprising! 🎉
    """
    
    print("🤖 Curator: Starting your wrapped creation...\n")
    print("-" * 70)
    print()
    
    # Stream the response for better UX
    try:
        # Create session if it doesn't exist
        session = await runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        if not session:
            session = await runner.session_service.create_session(
                app_name=runner.app_name,
                user_id=user_id,
                session_id=session_id
            )
        
        # Run agent and stream response
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=prompt)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTip: Make sure the CSV file exists and has the required columns:")
        print("  - date, show_name, duration_minutes, genre, completed, is_rewatch, session_id")
    
    print("\n")
    print("=" * 70)
    print("✨ Your Wrapped is ready!")
    print()
    print("💡 Want to explore more? Try interactive mode:")
    print("   python -m my_agent.interactive")


async def generate_quick_summary(csv_path: str, user_id: str = "user_001"):
    """
    Generates a quick summary without full wrapped experience.
    Useful for testing or quick insights.
    
    Args:
        csv_path: Path to the viewing history CSV file
        user_id: User identifier
    """
    print("⚡ Quick Summary Mode")
    print("=" * 70)
    
    session_id = f"quick_{user_id}"
    
    prompt = f"""
    Give me a quick 3-sentence summary of my viewing habits from: {csv_path}
    
    Include: total hours, top genre, and viewing personality type.
    Be friendly and casual!
    """
    
    try:
        # Create session if it doesn't exist
        session = await runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        if not session:
            session = await runner.session_service.create_session(
                app_name=runner.app_name,
                user_id=user_id,
                session_id=session_id
            )
        
        # Run agent and stream response
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=prompt)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 70)


def main():
    """
    Main entry point with CLI interface.
    """
    import sys
    
    # Check for CSV path
    if len(sys.argv) < 2:
        print("Usage: python -m my_agent.main <path_to_csv> [--quick]")
        print()
        print("Examples:")
        print("  python -m my_agent.main data/my_viewing_history.csv")
        print("  python -m my_agent.main data/sample_data.csv --quick")
        print()
        print("For interactive mode:")
        print("  python -m my_agent.interactive")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        print()
        print("💡 Tip: Create sample data with:")
        print("   python -m my_agent.create_sample_data")
        sys.exit(1)
    
    # Check for quick mode
    quick_mode = "--quick" in sys.argv
    
    if quick_mode:
        asyncio.run(generate_quick_summary(csv_path))
    else:
        asyncio.run(create_wrapped(csv_path))


if __name__ == "__main__":
    main()

