# 🏗️ Architecture Documentation

## System Overview

MyYear.AI is a **multi-agent AI system** that demonstrates advanced agent orchestration patterns using Google's Agent Development Kit (ADK). The system transforms raw viewing data into personalized, engaging narratives through specialized agents working together.

---

## 🎯 Design Principles

### 1. Agent Specialization
Each agent has a specific role and expertise:
- **Coordinator** - Orchestrates workflow and maintains context
- **Pattern Finder** - Data analysis and insights discovery
- **Storyteller** - Creative narrative generation
- **Quiz Master** - Interactive engagement
- **Social Creator** - Viral content generation

### 2. Separation of Concerns
- **Data Processing** - Pure Python tools (pandas, numpy)
- **Business Logic** - Custom tools with domain knowledge
- **AI Generation** - Gemini models via ADK agents
- **Orchestration** - Coordinator agent workflow

### 3. Scalability
- Stateless agents (can be scaled horizontally)
- Session-based state management
- Docker containerization
- Cloud-ready deployment

---

## 📊 Detailed Architecture

### Layer 1: Presentation Layer

```
┌─────────────────────────────────────────────┐
│          User Interfaces                    │
├─────────────────────────────────────────────┤
│ • CLI (main.py)                             │
│ • Interactive Chat (interactive.py)         │
│ • REST API (api.py)                         │
│ • Future: Web UI, Mobile App                │
└─────────────────────────────────────────────┘
```

**Key Features:**
- Multiple interface options
- Streaming responses for UX
- Session management
- Error handling

### Layer 2: Agent Orchestration Layer

```
┌─────────────────────────────────────────────┐
│      Coordinator Agent                      │
│      (agents/coordinator_agent.py)          │
├─────────────────────────────────────────────┤
│                                             │
│  Responsibilities:                          │
│  • Parse user intent                        │
│  • Delegate to sub-agents                   │
│  • Maintain conversation context            │
│  • Synthesize multi-agent responses         │
│  • Handle errors gracefully                 │
│                                             │
│  Model: Gemini 2.5 Flash                    │
│  Reason: Fast coordination, good reasoning  │
└─────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
        ▼            ▼            ▼            ▼
```

### Layer 3: Specialized Agents

#### Pattern Finder Agent
```
┌─────────────────────────────────────────────┐
│      Pattern Finder Agent                   │
│      (agents/pattern_finder_agent.py)       │
├─────────────────────────────────────────────┤
│  Purpose: Data analysis and discovery       │
│                                             │
│  Tools:                                     │
│  • read_viewing_data                        │
│  • calculate_stats                          │
│  • get_personality                          │
│  • analyze_evolution                        │
│  • get_date_viewing                         │
│                                             │
│  Model: Gemini 2.5 Flash                    │
│  Reason: Fast processing, tool use          │
└─────────────────────────────────────────────┘
```

#### Storyteller Agent
```
┌─────────────────────────────────────────────┐
│      Storyteller Agent                      │
│      (agents/storyteller_agent.py)          │
├─────────────────────────────────────────────┤
│  Purpose: Creative narrative generation     │
│                                             │
│  Tools: None (pure generation)              │
│                                             │
│  Model: Gemini 2.5 Pro                      │
│  Reason: Superior creative writing,         │
│          emotional depth, story structure   │
└─────────────────────────────────────────────┘
```

#### Quiz Agent
```
┌─────────────────────────────────────────────┐
│      Quiz Agent                             │
│      (agents/quiz_agent.py)                 │
├─────────────────────────────────────────────┤
│  Purpose: Interactive engagement            │
│                                             │
│  Tools:                                     │
│  • get_random_viewing_date                  │
│  • compare_guess_to_reality                 │
│                                             │
│  Model: Gemini 2.5 Flash                    │
│  Reason: Fast, playful interactions         │
└─────────────────────────────────────────────┘
```

#### Social Agent
```
┌─────────────────────────────────────────────┐
│      Social Agent                           │
│      (agents/social_agent.py)               │
├─────────────────────────────────────────────┤
│  Purpose: Viral content generation          │
│                                             │
│  Tools: None (pure generation)              │
│                                             │
│  Model: Gemini 2.5 Flash                    │
│  Reason: Fast, creative social content      │
└─────────────────────────────────────────────┘
```

### Layer 4: Tool Layer

```
┌─────────────────────────────────────────────┐
│          Custom Tools                       │
│          (tools/)                           │
├─────────────────────────────────────────────┤
│                                             │
│  CSV Tools (csv_tools.py):                  │
│  • read_viewing_history                     │
│  • calculate_personal_stats                 │
│  • get_viewing_by_date                      │
│                                             │
│  Personality Tools (personality_tools.py):  │
│  • determine_viewing_personality            │
│  • analyze_viewing_evolution                │
│                                             │
│  Technology: pandas, numpy                  │
└─────────────────────────────────────────────┘
```

### Layer 5: State Management

```
┌─────────────────────────────────────────────┐
│      Session Service                        │
│      (InMemorySessionService)               │
├─────────────────────────────────────────────┤
│                                             │
│  Purpose:                                   │
│  • Store conversation history               │
│  • Maintain user context                    │
│  • Enable multi-turn dialogue               │
│  • Cache uploaded data                      │
│                                             │
│  Type: In-memory (dev)                      │
│  Production: Redis/Firestore               │
└─────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### Flow 1: Generate Wrapped

```
1. User Request
   └─> python -m my_agent.main data.csv

2. Main Entry Point (main.py)
   └─> Loads CSV path
   └─> Creates session
   └─> Sends to Coordinator

3. Coordinator Agent
   └─> Parses request
   └─> Delegates to Pattern Finder
   
4. Pattern Finder Agent
   └─> Tool: read_viewing_data
   └─> Tool: calculate_stats
   └─> Tool: get_personality
   └─> Tool: analyze_evolution
   └─> Returns structured insights

5. Coordinator Agent
   └─> Receives insights
   └─> Delegates to Storyteller
   
6. Storyteller Agent
   └─> Receives data
   └─> Generates narrative
   └─> Returns story

7. Coordinator Agent
   └─> Delegates to Social Agent
   
8. Social Agent
   └─> Receives insights + story
   └─> Generates 3-5 social posts
   └─> Returns posts

9. Coordinator Agent
   └─> Synthesizes all responses
   └─> Formats final wrapped
   └─> Streams to user

10. User Output
    └─> Personalized wrapped displayed
```

### Flow 2: Interactive Chat

```
1. User Opens Chat
   └─> python -m my_agent.interactive data.csv

2. Interactive Module
   └─> Creates persistent session
   └─> Sends initialization prompt

3. Coordinator Agent
   └─> Delegates to Pattern Finder
   └─> Loads data into session
   └─> Returns greeting

4. User Sends Message
   └─> "What was my most watched show?"

5. Coordinator Agent
   └─> Retrieves session context
   └─> Determines this is data query
   └─> Delegates to Pattern Finder

6. Pattern Finder Agent
   └─> Accesses cached data
   └─> Analyzes for answer
   └─> Returns structured response

7. Coordinator Agent
   └─> Adds personality to response
   └─> Maintains conversation tone
   └─> Streams response

8. User Sees Response
   └─> Session state updated
   └─> Context preserved for next turn
```

### Flow 3: Quiz Mode

```
1. User Starts Quiz
   └─> python -m my_agent.interactive data.csv --quiz

2. Coordinator Agent
   └─> Delegates to Quiz Agent

3. Quiz Agent
   └─> Tool: get_random_viewing_date
   └─> Generates question
   └─> Returns question to user

4. User Answers
   └─> "Was it Stranger Things?"

5. Quiz Agent
   └─> Tool: compare_guess_to_reality
   └─> Checks correctness
   └─> Generates feedback
   └─> Explains why it's interesting

6. Coordinator Agent
   └─> Adds warmth to feedback
   └─> Asks if user wants another question

[Loop continues...]
```

---

## 🔧 Technical Stack

### Core Technologies
- **Python 3.11+** - Modern Python features
- **Google ADK** - Agent framework
- **Gemini 2.5 Flash/Pro** - LLM models
- **Pandas/NumPy** - Data processing
- **FastAPI** - REST API
- **Uvicorn** - ASGI server

### Deployment
- **Docker** - Containerization
- **Google Cloud Run** - Serverless deployment
- **Google Container Registry** - Image storage

### Development
- **Git** - Version control
- **pytest** - Testing
- **black** - Code formatting
- **mypy** - Type checking

---

## 📈 Scalability Considerations

### Current Architecture (MVP)
- **Session Storage**: In-memory (single instance)
- **File Storage**: Local filesystem
- **Concurrency**: Single process

### Production Architecture (Future)

```
┌─────────────────────────────────────────────┐
│         Load Balancer (Cloud Run)           │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────┬────────────┐
    │                         │            │
    ▼                         ▼            ▼
┌─────────┐             ┌─────────┐  ┌─────────┐
│ Instance│             │ Instance│  │ Instance│
│    1    │             │    2    │  │    3    │
└────┬────┘             └────┬────┘  └────┬────┘
     │                       │            │
     └───────────┬───────────┴────────────┘
                 │
    ┌────────────┴────────────┬────────────┐
    ▼                         ▼            ▼
┌─────────┐             ┌─────────┐  ┌─────────┐
│  Redis  │             │ Cloud   │  │ Cloud   │
│ (State) │             │ Storage │  │ SQL     │
└─────────┘             └─────────┘  └─────────┘
```

**Changes for production:**
1. **Redis** for session storage (distributed)
2. **Cloud Storage** for file uploads
3. **Cloud SQL** for user data
4. **Cloud Pub/Sub** for async processing
5. **Monitoring** with Cloud Logging/Monitoring

---

## 🔒 Security Considerations

### API Keys
- Stored in environment variables
- Never committed to git
- Rotated regularly

### User Data
- CSV files stored temporarily
- Cleaned up after processing
- No persistent storage of personal data
- GDPR/privacy compliant

### API Security
- Rate limiting
- Input validation
- Error sanitization
- CORS configuration

---

## 🎯 Key Design Decisions

### Why Multi-Agent?

**Decision**: Use specialized agents instead of monolithic LLM
**Rationale**:
- Clear separation of concerns
- Different models for different tasks (Flash vs Pro)
- Better error handling and debugging
- Easier to extend with new capabilities
- Demonstrates advanced ADK concepts

### Why Custom Tools?

**Decision**: Build custom tools for data processing
**Rationale**:
- LLMs are poor at math and data analysis
- Deterministic results for accuracy
- Faster processing
- Lower costs
- Shows proper architecture

### Why Session Management?

**Decision**: Use InMemorySessionService for state
**Rationale**:
- Enable multi-turn conversations
- Remember context across interactions
- Better user experience
- Demonstrates ADK sessions concept

### Why Gemini Pro for Storytelling?

**Decision**: Use Pro model only for storytelling agent
**Rationale**:
- Pro has superior creative writing
- Better emotional depth and metaphors
- Worth the extra cost for quality
- Flash for everything else (cost-effective)

---

## 🚀 Future Enhancements

### Phase 2: Advanced Features
- [ ] Voice output (text-to-speech)
- [ ] Multi-language support
- [ ] Integration with streaming APIs
- [ ] Real-time viewing tracking
- [ ] Friend comparison features

### Phase 3: Enterprise
- [ ] Team/household accounts
- [ ] Admin dashboard
- [ ] Analytics and insights
- [ ] White-label solution
- [ ] B2B API

### Phase 4: Scale
- [ ] Redis for distributed state
- [ ] Cloud Storage integration
- [ ] Database for user profiles
- [ ] Caching layer (CDN)
- [ ] Auto-scaling

---

## 📊 Performance Metrics

### Response Times (Target)
- CLI Wrapped: < 30 seconds end-to-end
- Interactive Chat: < 2 seconds per response
- API Chat: < 3 seconds (with streaming < 500ms first token)
- Quiz Mode: < 1 second per turn

### Concurrency (Current)
- Single instance: ~10 concurrent users
- With scaling: 1000+ concurrent users

### Cost Optimization
- Use Flash model (90% of requests)
- Cache common responses
- Batch processing where possible
- Efficient data structures

---

This architecture demonstrates a **production-ready multi-agent system** that balances:
- ✅ Innovation (multi-agent orchestration)
- ✅ Practicality (cost-effective, fast)
- ✅ Scalability (cloud-ready)
- ✅ User Experience (streaming, sessions)
- ✅ Code Quality (clean, documented)


