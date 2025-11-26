"""
Main agent entry point for MyYear.AI
This file is kept for compatibility but the main implementation
is in agents/coordinator_agent.py

To run the agent:
    python -m my_agent.main data/my_viewing_history.csv
    
To run interactive mode:
    python -m my_agent.interactive data/my_viewing_history.csv
"""
from my_agent.agents.coordinator_agent import personal_curator

# Export the main agent for backwards compatibility
root_agent = personal_curator
__all__ = ['root_agent', 'personal_curator']
