"""
Custom Tools for CSV Processing
KEY CONCEPT: Custom tools for data analysis
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os


def read_viewing_history(file_path: str) -> Dict[str, Any]:
    """
    Reads viewing history CSV file and returns structured data.
    
    This is a CUSTOM TOOL demonstrating tool integration with ADK.
    
    Args:
        file_path: Path to the CSV file containing viewing history
        
    Returns:
        Dictionary with viewing data summary and raw data
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Calculate basic metrics
        total_hours = df['duration_minutes'].sum() / 60 if 'duration_minutes' in df.columns else 0
        unique_shows = df['show_name'].nunique() if 'show_name' in df.columns else 0
        
        return {
            "success": True,
            "total_rows": len(df),
            "columns": list(df.columns),
            "date_range": {
                "start": str(df['date'].min()) if 'date' in df.columns else None,
                "end": str(df['date'].max()) if 'date' in df.columns else None
            },
            "total_hours": round(total_hours, 2),
            "unique_shows": unique_shows,
            "sample_data": df.head(10).to_dict('records'),
            "raw_data": None,
            "summary_stats": {
                "by_genre": (
                    {k: float(v) for k, v in df.groupby('genre')['duration_minutes'].sum().items()}
                    if 'genre' in df.columns else {}
                ),
                "by_show_duration": (
                    {k: float(v) for k, v in df.groupby('show_name')['duration_minutes'].sum().head(20).items()}
                    if 'show_name' in df.columns else {}
                ),
                "top_shows_by_count": (
                    {k: int(v) for k, v in df['show_name'].value_counts().head(10).items()}
                    if 'show_name' in df.columns else {}
                ),
                "by_month": (
                    {str(k): float(v) for k, v in df.groupby(df['date'].dt.to_period('M'))['duration_minutes'].sum().items()}
                    if 'date' in df.columns else {}
                )
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to read CSV file: {e}"
        }


def calculate_personal_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates personalized viewing statistics.
    
    CUSTOM TOOL for statistical analysis.
    
    Args:
        data: List of viewing records
        
    Returns:
        Dictionary with calculated personal statistics
    """
    try:
        df = pd.DataFrame(data)
        
        # Basic stats
        total_views = len(df)
        total_hours = df['duration_minutes'].sum() / 60 if 'duration_minutes' in df.columns else 0
        
        # Genre analysis
        top_genres = {}
        if 'genre' in df.columns:
            top_genres = df['genre'].value_counts().head(5).to_dict()
        
        # Viewing patterns
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['day_of_week'] = df['date'].dt.day_name()
            df['hour'] = df['date'].dt.hour
            
            top_viewing_days = df['day_of_week'].value_counts().head(3).to_dict()
            avg_hour = int(df['hour'].mean())
        else:
            top_viewing_days = {}
            avg_hour = 0
        
        # Completion rate
        completion_rate = 0
        if 'completed' in df.columns:
            completion_rate = df['completed'].mean()
        
        # Binge behavior (episodes per session)
        avg_episodes_per_session = 0
        if 'session_id' in df.columns:
            episodes_per_session = df.groupby('session_id').size()
            avg_episodes_per_session = float(episodes_per_session.mean())
        
        # Rewatch behavior
        rewatch_count = 0
        if 'is_rewatch' in df.columns:
            rewatch_count = int(df['is_rewatch'].sum())
        
        # Show loyalty
        top_shows = {}
        if 'show_name' in df.columns:
            top_shows = df['show_name'].value_counts().head(5).to_dict()
        
        return {
            "success": True,
            "total_views": total_views,
            "total_hours": round(total_hours, 2),
            "top_genres": top_genres,
            "top_shows": top_shows,
            "top_viewing_days": top_viewing_days,
            "avg_viewing_hour": avg_hour,
            "completion_rate": round(completion_rate, 3),
            "avg_episodes_per_session": round(avg_episodes_per_session, 2),
            "rewatch_count": rewatch_count,
            "unique_shows": df['show_name'].nunique() if 'show_name' in df.columns else 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_viewing_by_date(data: List[Dict[str, Any]], target_date: str) -> Dict[str, Any]:
    """
    Gets viewing information for a specific date.
    Used for interactive quiz feature.
    
    Args:
        data: List of viewing records
        target_date: Date to query (YYYY-MM-DD format)
        
    Returns:
        Dictionary with viewing info for that date
    """
    try:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        target = pd.to_datetime(target_date)
        
        # Filter by date
        day_data = df[df['date'].dt.date == target.date()]
        
        if len(day_data) == 0:
            return {
                "success": True,
                "has_viewing": False,
                "message": f"No viewing activity on {target_date}"
            }
        
        # Get most watched show that day
        most_watched = day_data['show_name'].mode()[0] if 'show_name' in day_data.columns else "Unknown"
        episodes_watched = len(day_data)
        total_minutes = day_data['duration_minutes'].sum() if 'duration_minutes' in day_data.columns else 0
        
        return {
            "success": True,
            "has_viewing": True,
            "date": target_date,
            "most_watched_show": most_watched,
            "episodes_watched": int(episodes_watched),
            "total_minutes": int(total_minutes),
            "shows": day_data['show_name'].tolist() if 'show_name' in day_data.columns else []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


