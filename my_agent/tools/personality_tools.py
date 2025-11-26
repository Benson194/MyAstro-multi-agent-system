"""
Custom Tools for Viewing Personality Analysis
KEY CONCEPT: Custom tools with business logic
"""
from typing import Dict, Any, List


def determine_viewing_personality(stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determines user's viewing personality type based on their habits.
    
    CUSTOM TOOL with personality classification logic.
    
    Args:
        stats: Dictionary with viewing statistics
        
    Returns:
        Personality type with description, emoji, and traits
    """
    try:
        # Extract key metrics
        binge_score = stats.get('avg_episodes_per_session', 0)
        completion_rate = stats.get('completion_rate', 0)
        rewatch_count = stats.get('rewatch_count', 0)
        unique_shows = stats.get('unique_shows', 0)
        top_genres = stats.get('top_genres', {})
        genre_diversity = len(top_genres)
        
        # Personality classification logic
        personality = {}
        
        # The Dedicated Binger
        if binge_score > 3.5 and completion_rate > 0.7:
            personality = {
                "type": "The Dedicated Binger",
                "emoji": "🎬",
                "description": "You commit to shows and see them through. When you start, you FINISH.",
                "traits": ["loyal", "focused", "completion-driven", "marathon-ready"],
                "percentage": "Top 15% of viewers",
                "famous_match": "Like binging Breaking Bad in a weekend",
                "tagline": "I don't quit what I start"
            }
        
        # The Genre Explorer
        elif genre_diversity >= 4 and unique_shows > 10:
            personality = {
                "type": "The Genre Explorer",
                "emoji": "🗺️",
                "description": "You're all over the map! Variety is your spice of life.",
                "traits": ["curious", "open-minded", "adventurous", "diverse"],
                "percentage": "Top 25% in diversity",
                "famous_match": "Your watchlist looks like a streaming buffet",
                "tagline": "Why choose when you can try everything?"
            }
        
        # The Comfort Seeker
        elif rewatch_count > 5:
            personality = {
                "type": "The Comfort Seeker",
                "emoji": "☕",
                "description": "You know what you love and you love it again and again.",
                "traits": ["nostalgic", "loyal", "comfort-focused", "sentimental"],
                "percentage": "Top 20% in rewatches",
                "famous_match": "The Office is basically your roommate",
                "tagline": "If it ain't broke, watch it again"
            }
        
        # The Weekend Warrior
        elif stats.get('top_viewing_days', {}).get('Saturday', 0) > 20 or \
             stats.get('top_viewing_days', {}).get('Sunday', 0) > 20:
            personality = {
                "type": "The Weekend Warrior",
                "emoji": "🏋️",
                "description": "You save your binging for the weekend. Work hard, watch harder.",
                "traits": ["disciplined", "balanced", "ritualistic", "strategic"],
                "percentage": "Classic weekend lifestyle",
                "famous_match": "Saturday night is sacred screen time",
                "tagline": "Weekends are for watching"
            }
        
        # The Night Owl
        elif stats.get('avg_viewing_hour', 0) >= 22:
            personality = {
                "type": "The Night Owl",
                "emoji": "🦉",
                "description": "Your prime time is when everyone else is sleeping.",
                "traits": ["nocturnal", "independent", "peaceful", "introspective"],
                "percentage": "Top 30% latest viewers",
                "famous_match": "3am and one more episode",
                "tagline": "The night is young and full of episodes"
            }
        
        # The Selective Curator
        elif completion_rate < 0.5 and unique_shows > 15:
            personality = {
                "type": "The Selective Curator",
                "emoji": "🎯",
                "description": "You're not afraid to quit. Life's too short for bad TV.",
                "traits": ["discerning", "efficient", "decisive", "quality-focused"],
                "percentage": "Top 10% most selective",
                "famous_match": "Three episode rule enforcer",
                "tagline": "I know what I like"
            }
        
        # The Casual Viewer (default)
        else:
            personality = {
                "type": "The Casual Viewer",
                "emoji": "😎",
                "description": "You watch for fun, not commitment. Chill vibes only.",
                "traits": ["relaxed", "spontaneous", "low-pressure", "flexible"],
                "percentage": "Perfectly balanced",
                "famous_match": "Whatever's on, you're down",
                "tagline": "Just here for a good time"
            }
        
        # Add metrics to personality
        personality["metrics"] = {
            "binge_score": round(binge_score, 2),
            "completion_rate": round(completion_rate * 100, 1),
            "rewatch_count": rewatch_count,
            "genre_diversity": genre_diversity
        }
        
        return {
            "success": True,
            "personality": personality
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "personality": {
                "type": "The Mystery Viewer",
                "emoji": "❓",
                "description": "Your viewing habits are enigmatic!",
                "traits": ["mysterious"],
                "tagline": "Too complex to categorize"
            }
        }


def analyze_viewing_evolution(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes how viewing habits evolved over the year.
    
    Args:
        data: List of viewing records
        
    Returns:
        Dictionary describing viewing evolution
    """
    try:
        import pandas as pd
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Split year into quarters
        df['quarter'] = df['date'].dt.quarter
        
        # Analyze genre shifts by quarter
        evolution = {}
        for quarter in sorted(df['quarter'].unique()):
            quarter_data = df[df['quarter'] == quarter]
            top_genre = quarter_data['genre'].mode()[0] if 'genre' in quarter_data.columns and len(quarter_data) > 0 else "Unknown"
            top_show = quarter_data['show_name'].mode()[0] if 'show_name' in quarter_data.columns and len(quarter_data) > 0 else "Unknown"
            
            quarter_name = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"][quarter - 1]
            
            evolution[quarter_name] = {
                "top_genre": top_genre,
                "top_show": top_show,
                "total_views": len(quarter_data)
            }
        
        # Detect transformation
        quarters = list(evolution.keys())
        if len(quarters) >= 2:
            first_genre = evolution[quarters[0]]['top_genre']
            last_genre = evolution[quarters[-1]]['top_genre']
            
            if first_genre != last_genre:
                transformation = f"From {first_genre} to {last_genre}"
            else:
                transformation = f"Consistent {first_genre} fan all year"
        else:
            transformation = "Not enough data for evolution analysis"
        
        return {
            "success": True,
            "evolution": evolution,
            "transformation": transformation
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


