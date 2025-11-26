"""
Quiz Agent
KEY CONCEPT: Interactive agent for Q&A with session management
"""
from typing import Any, Dict, List
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from my_agent.tools.csv_tools import get_viewing_by_date
import random
from datetime import datetime, timedelta


def get_random_viewing_date(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Picks a random date from viewing history for quiz questions.
    
    Args:
        data: List of viewing records
        
    Returns:
        Random date with viewing activity
    """
    import pandas as pd
    
    try:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Get unique dates
        unique_dates = df['date'].dt.date.unique()
        
        if len(unique_dates) == 0:
            return {
                "success": False,
                "message": "No viewing data found"
            }
        
        # Pick random date
        random_date = random.choice(unique_dates)
        
        # Get viewing info for that date
        date_str = random_date.strftime('%Y-%m-%d')
        viewing_info = get_viewing_by_date(data, date_str)
        
        return {
            "success": True,
            "date": date_str,
            "date_formatted": random_date.strftime('%B %d, %Y'),
            "viewing_info": viewing_info
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def compare_guess_to_reality(user_guess: str, actual_show: str)-> Dict[str, Any]:
    """
    Compares user's guess to actual viewing data.
    
    Args:
        user_guess: What the user guessed
        actual_show: What they actually watched
        
    Returns:
        Comparison result with fun feedback
    """
    # Normalize strings for comparison
    guess_normalized = user_guess.lower().strip()
    actual_normalized = actual_show.lower().strip()
    
    # Check if correct
    is_correct = guess_normalized in actual_normalized or actual_normalized in guess_normalized
    
    # Generate feedback
    if is_correct:
        feedback = [
            "🎯 Nailed it! Your memory is impressive!",
            "✨ Correct! You know yourself well!",
            "🎉 Yes! You remember perfectly!",
            "👏 That's right! Great memory!"
        ]
    else:
        feedback = [
            "😅 Not quite, but close guess!",
            "🤔 Interesting guess, but not this time!",
            "💭 Good try! Want to know the real answer?",
            "🎲 Nope, but that would've been cool!"
        ]
    
    return {
        "is_correct": is_correct,
        "feedback": random.choice(feedback),
        "user_guess": user_guess,
        "actual_show": actual_show
    }


# Quiz Agent Definition
quiz_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='quiz_agent',
    description='Creates fun interactive quiz about user viewing habits',
    
    instruction='''You are an engaging quiz master who creates playful, 
    interactive quizzes about viewing habits.
    
    Quiz Types You Can Create:
    1. "Guess what you watched on [date]" - Memory test
    2. "True or False about your habits" - Fun facts
    3. "Your viewing personality test" - Self-discovery
    4. "How well do you know your year?" - Trivia
    
    When creating questions:
    - Make them fun and engaging, not clinical
    - Use specific dates and shows for authenticity
    - Build anticipation before revealing answers
    - Celebrate correct guesses enthusiastically
    - Be encouraging with wrong guesses
    
    After user answers:
    - Reveal the truth with flair and surprise
    - Explain WHY it's interesting or meaningful
    - Connect it to their viewing personality
    - Keep it light, fun, and judgment-free
    
    Example interaction flow:
    Q: "Do you remember what you binged on March 15th? 🤔"
    [User: "Hmm, Stranger Things?"]
    A: "Close vibe! It was actually The Crown - you were in your 
    royal drama phase! 👑 You watched 6 episodes that day. 
    That was the start of your prestige TV era!"
    
    Tools available:
    - get_random_viewing_date: Get a random date for questions
    - compare_guess_to_reality: Check if user's guess is correct
    
    Always be encouraging, fun, and make the user feel good about 
    their viewing habits!
    ''',
    
    tools=[FunctionTool(get_random_viewing_date), FunctionTool(compare_guess_to_reality)],
)

