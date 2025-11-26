# 🎬 MyAstro Watch History AI Agent

> A multi-agent AI system for Astro users to interact with their MyAstro app watch history. Built for Malaysia's largest pay TV operator using Google's Agent Development Kit (ADK) and Gemini models.

[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google)](https://github.com/google/adk)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Astro Malaysia](https://img.shields.io/badge/Astro-Malaysia-red)](https://www.astro.com.my)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Concepts Demonstrated](#-key-concepts-demonstrated)
- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Demo](#-demo)

---

## 🎯 Problem Statement

**Company Context:**
This agent is built for **Astro Malaysia** - the largest pay TV operator in Malaysia, serving millions of subscribers through their MyAstro app.

**The Challenge:**
Astro users watch hundreds of hours of content through MyAstro each year but have no meaningful way to:
- Understand their viewing habits and patterns across Astro's channels
- Reflect on their entertainment journey with Astro content
- Discover personalized insights about their preferences
- Interact conversationally with their watch history
- Get personalized recommendations based on viewing behavior

**Current Pain Points for Astro Users:**
- MyAstro app only shows "Continue Watching" lists
- No personality insights or viewing pattern analysis
- Watch history data exists but isn't meaningful or actionable
- Generic recommendations don't leverage full viewing history
- No interactive way to explore and understand viewing habits
- Users can't easily query their watch history ("What did I watch last Tuesday?")

**Business Opportunity for Astro:**
- Increase user engagement with MyAstro app
- Provide value-added AI features to subscribers
- Differentiate from competing streaming services
- Drive content discovery and viewing time
- Create shareable "Wrapped" experiences to boost brand awareness

---

## 💡 Solution

**MyAstro Watch History AI Agent** is a multi-agent system that transforms Astro viewing data into:
- 📊 **Personalized Analytics** - Viewing patterns, habits, and personality across Astro channels
- 📖 **Narrative Story** - A compelling story of the user's year with Astro content
- 🎮 **Interactive Quiz** - Test memory and discover insights about viewing habits
- 📱 **Shareable Content** - Social media-ready posts to promote Astro engagement
- 💬 **Conversational AI** - Natural language interface to query watch history
  - "What did I watch last Friday?"
  - "What's my most-watched Astro channel?"
  - "When did I start watching [show name]?"

### Why Multi-Agent Architecture?

Instead of a single AI doing everything, we use **specialized agents** that work together for Astro users:
- **Coordinator Agent** - Orchestrates the team and provides conversational interface
- **Pattern Finder Agent** - Analyzes MyAstro watch history and discovers insights
- **Storyteller Agent** - Creates compelling narratives about viewing journey
- **Quiz Agent** - Generates interactive questions about viewing habits
- **Social Agent** - Creates shareable "Astro Wrapped" content

This architecture allows each agent to specialize in its domain while providing a seamless experience for Astro subscribers.

---

## 🔑 Key Concepts Demonstrated

This project showcases **6 key ADK concepts**:

### 1. ✅ Multi-Agent System
- **5 specialized agents** working together
- Sequential agent orchestration
- Agent-to-agent communication
- Clear separation of concerns

### 2. ✅ Custom Tools
- `read_viewing_history` - CSV data processing
- `calculate_personal_stats` - Statistical analysis
- `determine_viewing_personality` - Personality classification
- `analyze_viewing_evolution` - Temporal analysis
- `get_viewing_by_date` - Date-specific queries

### 3. ✅ Sessions & Memory
- `InMemorySessionService` for state management
- Persistent conversations across multiple turns
- Context retention for interactive chat
- Session-based user experiences

### 4. ✅ Built-in Tools
- Gemini 2.5 Flash for fast responses
- Gemini 2.5 Pro for creative storytelling
- Structured output generation

### 5. ✅ Agent Deployment
- FastAPI REST API
- Docker containerization
- Google Cloud Run configuration
- Deployment automation scripts

### 6. ✅ Streaming Responses
- Real-time output generation
- Server-Sent Events (SSE)
- Improved user experience with perceived speed

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER REQUEST                         │
│         "Tell me about my year in watching!"            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          PERSONAL CURATOR AGENT (Coordinator)           │
│         - Gemini 2.5 Flash                              │
│         - Orchestrates sub-agents                       │
│         - Maintains session state                       │
│         - Friendly, conversational interface            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
┌──────────────┐ ┌──────────┐ ┌────────┐ ┌───────────┐
│  Pattern     │ │Story-    │ │ Quiz   │ │  Social   │
│  Finder      │ │teller    │ │ Agent  │ │  Agent    │
│              │ │          │ │        │ │           │
│ - Gemini     │ │- Gemini  │ │- Gemini│ │ - Gemini  │
│   Flash      │ │  Pro     │ │  Flash │ │   Flash   │
│ - Custom     │ │- Creative│ │- Inter-│ │ - Viral   │
│   Tools      │ │  Writing │ │  active│ │   Content │
└──────┬───────┘ └─────┬────┘ └───┬────┘ └─────┬─────┘
       │               │          │            │
       ▼               ▼          ▼            ▼
   [CSV Tools]   [Narrative]  [Quiz Tools] [Social Posts]
   
   
┌─────────────────────────────────────────────────────────┐
│                    SESSION SERVICE                      │
│         InMemorySessionService (State Management)       │
│         - Conversation history                          │
│         - User context                                  │
│         - Multi-turn interactions                       │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User uploads viewing history CSV** → Stored in session
2. **Coordinator receives request** → Analyzes intent
3. **Delegates to Pattern Finder** → Loads data, calculates stats, determines personality
4. **Passes insights to Storyteller** → Creates narrative from data
5. **Social Agent generates posts** → Viral-ready content
6. **Quiz Agent creates questions** → Interactive experience
7. **Coordinator synthesizes** → Cohesive wrapped experience

---

## ✨ Features

### 📊 Viewing Analytics
- Total hours watched
- Top shows and genres
- Viewing patterns (time of day, day of week)
- Completion rates
- Binge behavior analysis
- Rewatch patterns

### 🎭 Personality Types
- **The Dedicated Binger** - Finishes what they start
- **The Genre Explorer** - Diverse taste
- **The Comfort Seeker** - Rewatches favorites
- **The Weekend Warrior** - Weekend viewing rituals
- **The Night Owl** - Late-night viewer
- **The Selective Curator** - High standards

### 📖 Narrative Story
- Year-long journey with story arc
- Key moments and discoveries
- Evolution and transformation
- Emotional and engaging writing
- Shareable and quotable

### 🎮 Interactive Features
- Memory quiz about viewing dates
- True/False habit questions
- Personality discovery
- Conversational Q&A

### 📱 Social Sharing
- Instagram-ready posts
- Twitter-optimized content
- Viral-friendly formatting
- Hashtag suggestions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google API Key (for Gemini models)
- Access to MyAstro watch history data (CSV format)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file and add your GOOGLE_API_KEY
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Generate Sample Data (For Testing)

```bash
# Create sample MyAstro viewing history
python -m my_agent.create_sample_data
```

This creates `data/my_viewing_history.csv` with 500 realistic Astro viewing records for testing purposes.

---

## 📖 Usage

### 1. Generate Astro Wrapped Experience

```bash
# Full MyAstro wrapped experience
python -m my_agent.main data/my_viewing_history.csv

# Quick summary mode
python -m my_agent.main data/my_viewing_history.csv --quick
```

**Output for Astro Users:**
- Viewing analytics and personality based on Astro content
- Narrative story of the year with Astro
- Shareable "Astro Wrapped" social posts
- Viewing evolution analysis across Astro channels

### 2. Interactive Chat Mode (MyAstro Watch History Query)

```bash
# Start interactive conversation about MyAstro watch history
python -m my_agent.interactive data/my_viewing_history.csv
```

**Example interactions for Astro users:**
```
You: What was my most-watched genre on Astro?
🤖 Curator: You're a thriller addict! You watched 45 thriller 
shows on Astro this year, making up 35% of your viewing. Your 
top picks were on channels 481 and 411! 🕵️

You: What did I watch last Friday?
🤖 Curator: Last Friday, you watched 3 episodes of [Show Name] 
on Astro channel 401 between 8 PM and 10 PM. You're really into 
that series! 🎬

You: Which Astro channel do I watch most?
🤖 Curator: Channel 481 is your go-to! You've spent 45 hours 
there this year, mostly watching drama series in the evenings.
```

### 3. Quiz Mode

```bash
# Play interactive quiz
python -m my_agent.interactive data/my_viewing_history.csv --quiz
```

**Sample quiz:**
```
🎯 Do you remember what you watched most on March 15, 2024?

Your answer: Stranger Things?

🤖 Curator: Close vibe! It was actually True Detective - you 
watched 4 episodes that night! That was the start of your 
thriller obsession. From that day on, 60% of your viewing 
became mystery/thriller content! 🔍
```

## 📁 Project Structure

```
agent/  (MyAstro Watch History AI Agent)
├── my_agent/
│   ├── __init__.py
│   ├── __main__.py              # Package entry point
│   ├── agent.py                 # Main agent export
│   ├── main.py                  # CLI wrapped generation
│   ├── interactive.py           # Interactive chat mode for Astro users
│   ├── api.py                   # FastAPI server for MyAstro integration
│   ├── create_sample_data.py    # Sample Astro data generator
│   │
│   ├── agents/                  # Multi-agent system
│   │   ├── coordinator_agent.py      # Main orchestrator
│   │   ├── pattern_finder_agent.py   # Astro watch history analysis
│   │   ├── storyteller_agent.py      # Narrative creation
│   │   ├── quiz_agent.py             # Interactive Q&A
│   │   └── social_agent.py           # Astro Wrapped social content
│   │
│   └── tools/                   # Custom tools
│       ├── csv_tools.py              # MyAstro data processing
│       └── personality_tools.py      # Viewing personality analysis
│
├── data/
│   └── my_viewing_history.csv   # Sample MyAstro watch history
│
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container image for deployment
├── .dockerignore               # Docker exclusions
├── deploy.sh                   # Cloud deployment script
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git exclusions (includes .env)
└── README.md                   # This file
```

---

## 🎥 Demo

### Sample Output (MyAstro User Experience)

```
🎬 Welcome to MyAstro Watch History AI - Your Personalized Viewing Wrapped!
======================================================================

🤖 Curator: Starting your Astro wrapped creation...

----------------------------------------------------------------------

✨ Analyzing your viewing history...

[Pattern Finder Agent working...]
✓ Loaded 500 viewing records
✓ Calculated personal statistics
✓ Determined viewing personality

🎭 Your Viewing Personality: THE NIGHT OWL 🦉

You're part of an exclusive club - the top 30% of latest-night 
viewers! Your average viewing time is 10:47 PM. While others sleep, 
you're exploring new worlds on screen.

📊 Your Year in Numbers:
• Total Hours: 127.3 hours (that's like flying to Tokyo!)
• Shows Watched: 45 unique shows
• Episodes: 487 episodes
• Completion Rate: 73% (you value closure!)
• Rewatch Count: 8 shows (comfort viewing champion)
• Top Genre: Thriller (35% of viewing)

[Storyteller Agent creating your narrative...]

═══════════════════════════════════════════════════════════════════
📖 YOUR 2024 VIEWING STORY
═══════════════════════════════════════════════════════════════════

The Year You Became a Mystery Solver 🕵️

Your year started innocently - comfort comedies and familiar faces 
in January. The Office reruns, Friends marathons, the usual suspects.

But then March happened.

March 15th, to be exact. You discovered True Detective, and four 
episodes disappeared into that night like witnesses in a cold case. 
By morning, you weren't just a viewer anymore. You were a detective.

The transformation was swift. Your queue evolved from rom-coms to 
crime scenes. Mindhunter. Dark. Ozark. Stranger Things (again, but 
with new eyes). You weren't watching TV; you were solving puzzles, 
following clues, staying two steps ahead of the reveal.

By summer, your Saturday nights had a ritual: lights down, phone off, 
three episodes minimum. You'd discovered your viewing identity - the 
person who leans forward, not back. Who remembers details. Who gasps 
at twists but loves being fooled.

The numbers tell one story (127 hours, 45 shows, top 15% in completion 
rate). But the real story is simpler: you found what you love. And 
you leaned all the way in.

[Social Agent generating shareable content...]

📱 READY TO SHARE:

1. "I watched 127 hours this year and accidentally became a thriller 
   addict 🕵️ Started with The Office, ended solving murders. 
   Character development! #MyYearInWatching #ViewingPersonality"

2. "My viewing personality: The Night Owl 🦉 While you sleep, I'm 
   exploring fictional crime scenes at 11 PM. What's yours? #MyYearAI"

3. "March 15, 2024: The night True Detective changed everything. 
   Before: comedies. After: 45 thrillers and no regrets. 
   #PlotTwist #ViewingJourney"

══════════════════════════════════════════════════════════════════════
✨ Your Wrapped is ready!

💡 Want to explore more? Try interactive mode:
   python -m my_agent.interactive
```
## 🙏 Acknowledgments

- **Astro Malaysia** - Malaysia's largest pay TV operator
- Google Agent Development Kit (ADK)
- Google Gemini Models

**Made with ❤️ and 🤖 for Astro Malaysia using Google ADK**


