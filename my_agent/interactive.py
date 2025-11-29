"""
Interactive Chat Mode for MyYear.AI
KEY CONCEPTS:
- Session persistence for multi-turn conversations
- Memory across interactions
- Interactive Q&A with quiz agent
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


async def interactive_chat(csv_path: str, user_id: str = "user_001"):
    """
    Interactive Q&A session about viewing habits.
    
    KEY CONCEPT: Session-based interactive agent
    - Maintains conversation history
    - Remembers context from previous messages
    - Enables natural multi-turn dialogue
    
    Args:
        csv_path: Path to viewing history CSV
        user_id: User identifier for session
    """
    session_id = f"interactive_{user_id}"
    
    # Initialize with data
    init_prompt = f"""
    I want to chat about my viewing history from: {csv_path}
    
    Load my data so we can have an interactive conversation.
    Say hello and ask if I want to play a quiz or just chat!
    """
    
    print("🎮 MyYear.AI - Interactive Mode")
    print("=" * 70)
    print()
    
    # Initialize session
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
        
        # Send initial message
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=init_prompt)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
        print("\n")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        print("\nMake sure the CSV file exists and has valid data.")
        return
    
    # Interactive loop
    # KEY CONCEPT: Session maintains state across multiple turns
    print("-" * 70)
    print("💬 Type your messages below. Type 'quit', 'exit', or 'bye' to end.")
    print("-" * 70)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'done']:
                print("\n🤖 Curator: Thanks for chatting! Your viewing year is awesome! 👋")
                print()
                break
            
            # Send message to agent (session maintains context)
            print("🤖 Curator: ", end='', flush=True)
            
            has_response = False
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=types.UserContent(parts=[types.Part(text=user_input)])
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end='', flush=True)
                            has_response = True
            
            if not has_response:
                # If no text was printed, the agent might still be processing
                # Let's wait a moment and check the session
                print("[Processing...]")
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat ended. See you next time!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Let's continue...\n")


async def quiz_mode(csv_path: str, user_id: str = "user_001"):
    """
    Dedicated quiz mode for testing memory.
    
    Args:
        csv_path: Path to viewing history CSV
        user_id: User identifier
    """
    session_id = f"quiz_{user_id}"
    
    print("🎯 MyYear.AI - Quiz Mode")
    print("=" * 70)
    print()
    
    init_prompt = f"""
    I want to play a quiz game about my viewing history from: {csv_path}
    
    Create a fun quiz! Ask me 3-5 questions about:
    - What I watched on specific dates
    - My viewing patterns
    - My personality traits
    
    Make it fun and interactive! 🎮
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
        
        # Send initial quiz message
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=init_prompt)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
        print("\n")
        
        # Continue with answers
        print("-" * 70)
        print("Answer the questions above, or type 'skip' to skip")
        print("-" * 70)
        print()
        
        while True:
            user_answer = input("Your answer: ").strip()
            
            if not user_answer:
                continue
            
            if user_answer.lower() in ['quit', 'exit', 'done']:
                break
            
            print("🤖 Curator: ", end='', flush=True)
            
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=types.UserContent(parts=[types.Part(text=user_answer)])
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end='', flush=True)
            print("\n")
            
    except KeyboardInterrupt:
        print("\n\n👋 Quiz ended!")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """
    Main entry point for interactive mode.
    """
    import sys
    
    # Default to sample data if no path provided
    if len(sys.argv) < 2:
        # Look for sample data in data directory
        sample_path = "data/my_viewing_history.csv"
        if os.path.exists(sample_path):
            csv_path = sample_path
            print(f"📁 Using sample data: {sample_path}\n")
        else:
            print("Usage: python -m my_agent.interactive <path_to_csv> [--quiz]")
            print()
            print("Examples:")
            print("  python -m my_agent.interactive data/my_viewing_history.csv")
            print("  python -m my_agent.interactive data/sample_data.csv --quiz")
            print()
            print("💡 Create sample data first:")
            print("   python -m my_agent.create_sample_data")
            sys.exit(1)
    else:
        csv_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    
    # Check for quiz mode
    quiz_mode_flag = "--quiz" in sys.argv
    
    if quiz_mode_flag:
        asyncio.run(quiz_mode(csv_path))
    else:
        asyncio.run(interactive_chat(csv_path))


if __name__ == "__main__":
    main()

