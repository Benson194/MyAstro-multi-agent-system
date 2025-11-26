"""
Sample Data Generator for MyYear.AI
Creates realistic viewing history CSV for testing and demo purposes
"""
import pandas as pd
import random
from datetime import datetime, timedelta
import os


# Sample shows by genre
SHOWS_BY_GENRE = {
    "Thriller": ["Stranger Things", "True Detective", "Mindhunter", "Dark", "Ozark"],
    "Comedy": ["The Office", "Friends", "Brooklyn Nine-Nine", "Ted Lasso", "The Good Place"],
    "Drama": ["The Crown", "Breaking Bad", "Mad Men", "Succession", "The Bear"],
    "Sci-Fi": ["Black Mirror", "The Expanse", "Westworld", "Severance", "Foundation"],
    "Documentary": ["Making a Murderer", "Planet Earth", "Chef's Table", "The Last Dance", "Drive to Survive"],
    "Romance": ["Bridgerton", "Emily in Paris", "Love is Blind", "Virgin River", "Heartstopper"],
    "Crime": ["Narcos", "True Crime", "Only Murders in the Building", "Mare of Easttown", "The Sinner"],
    "Fantasy": ["The Witcher", "House of the Dragon", "The Rings of Power", "Shadow and Bone", "Wednesday"],
}


def generate_viewing_history(
    num_entries: int = 500,
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31"
) -> pd.DataFrame:
    """
    Generates realistic viewing history data.
    
    Args:
        num_entries: Number of viewing records to generate
        start_date: Start date for viewing history
        end_date: End date for viewing history
        
    Returns:
        DataFrame with viewing history
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    records = []
    current_session = 1
    episodes_in_session = 0
    favorite_shows = set()
    
    # Simulate viewing evolution (genre preferences change over time)
    # Q1: Comedy/Romance (comfort viewing)
    # Q2: Mix (exploring)
    # Q3: Thriller/Crime (discovery phase)
    # Q4: Mix with favorites (established preferences)
    
    for i in range(num_entries):
        # Generate random date within range
        days_between = (end - start).days
        random_days = random.randint(0, days_between)
        view_date = start + timedelta(days=random_days)
        
        # Determine genre based on time of year (simulate evolution)
        quarter = (view_date.month - 1) // 3 + 1
        
        if quarter == 1:
            # Q1: Comfort viewing
            genre_weights = {"Comedy": 0.4, "Romance": 0.3, "Drama": 0.3}
        elif quarter == 2:
            # Q2: Exploration
            genre_weights = {"Comedy": 0.2, "Drama": 0.2, "Thriller": 0.2, "Sci-Fi": 0.2, "Documentary": 0.2}
        elif quarter == 3:
            # Q3: Discovery of thriller/crime
            genre_weights = {"Thriller": 0.4, "Crime": 0.3, "Sci-Fi": 0.2, "Drama": 0.1}
        else:
            # Q4: Mix of established favorites
            genre_weights = {"Thriller": 0.3, "Drama": 0.2, "Comedy": 0.2, "Crime": 0.2, "Sci-Fi": 0.1}
        
        genre = random.choices(
            list(genre_weights.keys()),
            weights=list(genre_weights.values())
        )[0]
        
        show = random.choice(SHOWS_BY_GENRE[genre])
        
        # Track favorite shows (shows with 5+ episodes watched)
        if show in favorite_shows or random.random() > 0.7:
            favorite_shows.add(show)
        
        # Viewing time (biased towards evenings and weekends)
        if view_date.weekday() >= 5:  # Weekend
            hour = random.choices(
                range(10, 24),
                weights=[1,1,1,2,2,3,3,4,5,6,7,7,6,5]  # Peak at evening
            )[0]
        else:  # Weekday
            hour = random.choices(
                range(18, 24),
                weights=[1,2,3,4,5,6]  # After work
            )[0]
        
        view_datetime = view_date.replace(hour=hour, minute=random.randint(0, 59))
        
        # Episode duration (40-60 minutes)
        duration = random.randint(35, 65)
        
        # Completion rate (higher for favorites)
        if show in favorite_shows:
            completed = random.random() > 0.2  # 80% completion for favorites
        else:
            completed = random.random() > 0.4  # 60% completion otherwise
        
        # Rewatch (5% chance for favorites)
        is_rewatch = show in favorite_shows and random.random() < 0.05
        
        # Session tracking (binge behavior)
        if episodes_in_session == 0 or random.random() < 0.4:
            # New session
            current_session += 1
            episodes_in_session = random.randint(1, 6)  # 1-6 episodes per session
        
        episodes_in_session -= 1
        
        # Episode number
        episode_num = random.randint(1, 12)
        season_num = random.randint(1, 5)
        
        records.append({
            "date": view_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "show_name": show,
            "season": season_num,
            "episode": episode_num,
            "genre": genre,
            "duration_minutes": duration,
            "completed": completed,
            "is_rewatch": is_rewatch,
            "session_id": f"session_{current_session}",
            "day_of_week": view_datetime.strftime("%A"),
            "hour": hour
        })
    
    # Create DataFrame and sort by date
    df = pd.DataFrame(records)
    df = df.sort_values("date").reset_index(drop=True)
    
    return df


def create_sample_files():
    """
    Creates sample data files in the data directory.
    """
    # Create data directory if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    print("📊 Generating sample viewing history...")
    
    # Generate sample data
    df = generate_viewing_history(num_entries=500)
    
    # Save to CSV
    output_path = os.path.join(data_dir, "my_viewing_history.csv")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Created: {output_path}")
    print(f"   - {len(df)} viewing records")
    print(f"   - {df['show_name'].nunique()} unique shows")
    print(f"   - {df['date'].min()} to {df['date'].max()}")
    print(f"   - {df['duration_minutes'].sum() / 60:.1f} total hours")
    print()
    
    # Print sample
    print("📋 Sample data (first 5 rows):")
    print(df.head().to_string())
    print()
    
    print("🎉 Sample data created successfully!")
    print()
    print("Next steps:")
    print("  1. Generate your wrapped:")
    print("     python -m my_agent.main data/my_viewing_history.csv")
    print()
    print("  2. Try interactive mode:")
    print("     python -m my_agent.interactive data/my_viewing_history.csv")
    print()
    print("  3. Try quiz mode:")
    print("     python -m my_agent.interactive data/my_viewing_history.csv --quiz")


if __name__ == "__main__":
    create_sample_files()


