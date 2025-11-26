"""
Pattern Finder Agent
KEY CONCEPT: Specialized agent in multi-agent system with custom tools
"""
from typing import Any, Dict, List
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from my_agent.tools.csv_tools import (
    read_viewing_history, 
    calculate_personal_stats,
    get_viewing_by_date
)
from my_agent.tools.personality_tools import (
    determine_viewing_personality,
    analyze_viewing_evolution
)


# Wrap custom tools for ADK using FunctionTool
def read_viewing_data(file_path: str) -> Dict[str, Any]:
    """
    Reads user's viewing history from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Viewing history data with summary
    """
    return read_viewing_history(file_path)


def calculate_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates personalized viewing statistics.
    
    Args:
        data: List of viewing records
        
    Returns:
        Dictionary with calculated statistics
    """
    return calculate_personal_stats(data)


def get_personality(stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determines viewing personality type.
    
    Args:
        stats: Dictionary with viewing statistics
        
    Returns:
        Personality analysis with type and traits
    """
    return determine_viewing_personality(stats)


def analyze_evolution(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes how viewing habits evolved over time.
    
    Args:
        data: List of viewing records
        
    Returns:
        Evolution analysis by time period
    """
    return analyze_viewing_evolution(data)


def get_date_viewing(data: List[Dict[str, Any]], target_date: str) -> Dict[str, Any]:
    """
    Gets viewing information for a specific date (for quiz feature).
    
    Args:
        data: List of viewing records
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        What was watched on that date
    """
    return get_viewing_by_date(data, target_date)


# Pattern Finder Agent Definition
pattern_finder = Agent(
    model='gemini-2.5-flash-lite',
    name='pattern_finder',
    description='Discovers interesting patterns in personal viewing habits',
    
    instruction='''You are a pattern discovery specialist who finds cool insights 
    that users don't know about themselves.
    
    Your mission:
    - Discover viewing time patterns (night owl? morning person?)
    - Identify binge vs. casual viewing behavior
    - Track genre evolution over the year
    - Spot rewatch behavior and comfort shows
    - Find seasonal changes in viewing
    - Detect social vs. solo watching patterns
    
    Present findings like fun discoveries, not clinical analysis.
    
    Use these tools:
    - read_viewing_data: Load viewing history
    - calculate_stats: Get statistical analysis
    - get_personality: Determine personality type
    - analyze_evolution: Track changes over time
    - get_date_viewing: Get specific date info
    
    Always be enthusiastic about discoveries! Use emojis and friendly language.
    Frame insights positively and make them personally meaningful.
    ''',
    
    # KEY CONCEPT: Custom tools integration
    tools=[
        FunctionTool(read_viewing_data),
        FunctionTool(calculate_stats),
        FunctionTool(get_personality),
        FunctionTool(analyze_evolution),
        FunctionTool(get_date_viewing)
    ],
)

