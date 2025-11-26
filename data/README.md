# Data Directory

This directory contains viewing history data files.

## Creating Sample Data

Run the sample data generator:

```bash
python -m my_agent.create_sample_data
```

This will create `my_viewing_history.csv` with realistic sample data.

## CSV Format

Your viewing history CSV should have these columns:

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | When the content was watched (YYYY-MM-DD HH:MM:SS) |
| `show_name` | string | Name of the show |
| `season` | int | Season number |
| `episode` | int | Episode number |
| `genre` | string | Genre (Thriller, Comedy, Drama, etc.) |
| `duration_minutes` | int | How long you watched (in minutes) |
| `completed` | boolean | Whether you finished the episode |
| `is_rewatch` | boolean | Whether this was a rewatch |
| `session_id` | string | Session identifier (for binge tracking) |
| `day_of_week` | string | Day name (Monday, Tuesday, etc.) |
| `hour` | int | Hour of day (0-23) |

## Example Row

```csv
date,show_name,season,episode,genre,duration_minutes,completed,is_rewatch,session_id,day_of_week,hour
2024-03-15 22:30:00,True Detective,1,3,Thriller,58,True,False,session_42,Friday,22
```

## Privacy Note

This directory is in `.gitignore` to protect your personal data. Sample data is for demo purposes only.


