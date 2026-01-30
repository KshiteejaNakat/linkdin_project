# 🏗️ Architecture Documentation

## Overview

The Adaptive AI Career Architect is built on a modular, agent-based architecture designed for scalability, maintainability, and extensibility. This document provides a comprehensive overview of the system's design.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Streamlit UI                              │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   │   │
│  │  │  Profile  │ │  Results  │ │Optimization│ │ Portfolio │   │   │
│  │  │   Input   │ │  Display  │ │   Panel   │ │  Preview  │   │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Orchestrator Agent                          │   │
│  │         (Coordinates all specialized agents)                 │   │
│  └──────────┬──────────┬───────────┬───────────┬───────────────┘   │
│             │          │           │           │                    │
│       ┌─────▼────┐ ┌───▼───┐ ┌────▼────┐ ┌────▼────┐              │
│       │ Profile  │ │Content│ │Portfolio│ │Optimize │              │
│       │ Analyzer │ │ Gen   │ │  Agent  │ │  Agent  │              │
│       └──────────┘ └───────┘ └─────────┘ └─────────┘              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FEATURE LAYER                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │   Profile    │ │   Career     │ │   LinkedIn   │ │  Portfolio │ │
│  │ Intelligence │ │     DNA      │ │  Optimizer   │ │   Builder  │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
│  ┌──────────────┐                                                   │
│  │   Feedback   │                                                   │
│  │     Loop     │                                                   │
│  └──────────────┘                                                   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          MODEL LAYER                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  HuggingFace Client                          │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐               │   │
│  │  │   Text     │ │ Embeddings │ │Classification│              │   │
│  │  │ Generation │ │            │ │              │              │   │
│  │  └────────────┘ └────────────┘ └────────────┘               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Model Selector                            │   │
│  │      (Chooses optimal model for each task)                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SQLAlchemy ORM                            │   │
│  │  ┌──────┐ ┌───────┐ ┌──────────┐ ┌────────────┐             │   │
│  │  │ User │ │Profile│ │CareerDNA │ │Optimization│             │   │
│  │  └──────┘ └───────┘ └──────────┘ └────────────┘             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Layer

#### Streamlit UI (`src/ui/`)
- **main_app.py**: Application entry point and layout management
- **components/**: Modular UI components
  - `profile_input.py`: Multi-source profile data collection
  - `results_display.py`: Career DNA visualization
  - `optimization_panel.py`: LinkedIn content optimization
  - `portfolio_preview.py`: Generated portfolio preview

**Design Pattern**: Component-based architecture with state management via Streamlit's session state.

### 2. Agent Layer

#### Base Agent (`src/agents/base_agent.py`)
Abstract base class implementing the core agent pattern:

```python
class BaseAgent(ABC):
    """
    State Machine: IDLE → THINKING → EXECUTING → COMPLETED/ERROR
    
    Methods:
    - think(context): Analyze input and plan actions
    - execute(action): Perform planned action
    - run(input_data): Complete agent lifecycle
    """
```

#### Orchestrator Agent (`src/agents/orchestrator_agent.py`)
Central coordinator that:
- Manages agent lifecycle
- Routes requests to specialized agents
- Aggregates results from multiple agents
- Handles error recovery and fallbacks

#### Specialized Agents
| Agent | Responsibility |
|-------|---------------|
| ProfileAnalyzerAgent | Extract insights from raw profile data |
| ContentGeneratorAgent | Generate optimized text content |
| PortfolioAgent | Coordinate portfolio generation |
| OptimizationAgent | Suggest profile improvements |

### 3. Feature Layer

#### Profile Intelligence (`src/features/profile_intelligence/`)
- **linkedin_scraper.py**: Extract LinkedIn profile data
- **pattern_extractor.py**: Identify successful profile patterns
- **market_analyzer.py**: Industry trend and demand analysis

#### Career DNA (`src/features/career_dna/`)
- **resume_parser.py**: Parse PDF/DOCX resumes
- **github_analyzer.py**: Analyze GitHub contributions
- **dna_builder.py**: Merge sources into unified profile

#### LinkedIn Optimizer (`src/features/linkedin_optimizer/`)
- **headline_generator.py**: AI-powered headline generation
- **about_generator.py**: Professional summary optimization
- **experience_optimizer.py**: Achievement quantification

#### Portfolio Builder (`src/features/portfolio_builder/`)
- **content_generator.py**: Portfolio content creation
- **layout_selector.py**: Template selection logic
- **react_generator.py**: React component generation

#### Feedback Loop (`src/features/feedback_loop/`)
- **metrics_collector.py**: Engagement metrics tracking
- **adaptation_engine.py**: Continuous improvement recommendations

### 4. Model Layer

#### HuggingFace Client (`src/models/huggingface_client.py`)
Unified interface for AI model interactions:

```python
class HuggingFaceClient:
    async def generate(prompt, config) → str
    async def embed_text(text) → List[float]
    async def classify(text, labels) → Dict
```

**Features**:
- Async API calls
- Automatic retry with backoff
- Local model fallback
- Response caching

#### Model Selector (`src/models/model_selector.py`)
Intelligent model selection based on:
- Task type (generation, embedding, classification)
- Performance requirements (fast, balanced, quality)
- Use case specifics

### 5. Data Layer

#### Database Models (`src/database/models.py`)
```
User
├── Profile (1:N)
│   ├── CareerDNA (1:1)
│   ├── Optimization (1:N)
│   └── Portfolio (1:N)
└── Metrics (1:N)
```

#### Repository Pattern (`src/database/repositories.py`)
Clean separation between business logic and data access:
- `UserRepository`
- `ProfileRepository`
- `CareerDNARepository`
- `OptimizationRepository`

## Data Flow

### Profile Optimization Flow

```
1. User Input
   │
   ▼
2. Profile Collection
   ├── Resume Upload → ResumeParser
   ├── LinkedIn URL → LinkedInScraper
   └── Manual Entry → Direct Mapping
   │
   ▼
3. Career DNA Building
   │  ├── Merge Data Sources
   │  ├── Extract Skills
   │  ├── Identify Patterns
   │  └── Calculate Market Fit
   │
   ▼
4. LinkedIn Optimization
   │  ├── Generate Headlines (HuggingFace)
   │  ├── Optimize About Section
   │  └── Enhance Experience Bullets
   │
   ▼
5. Portfolio Generation
   │  ├── Select Layout
   │  ├── Generate Content
   │  └── Create React Components
   │
   ▼
6. Export & Deployment
```

## Agent Communication

Agents communicate through a message-passing system:

```python
@dataclass
class AgentMessage:
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str  # request, response, error
    timestamp: datetime
```

### Message Flow Example

```
OrchestratorAgent
    │
    ├──[request]──► ProfileAnalyzerAgent
    │                    │
    │    ◄──[response]───┘
    │
    ├──[request]──► ContentGeneratorAgent
    │                    │
    │    ◄──[response]───┘
    │
    └──[aggregate]──► Return to UI
```

## Error Handling Strategy

### Graceful Degradation
1. **API Failures**: Fall back to template-based generation
2. **Model Timeouts**: Use cached responses or simplified models
3. **Data Errors**: Validate and sanitize with sensible defaults

### Error Propagation

```python
try:
    result = await agent.run(input)
except AgentError as e:
    # Log and notify
    logger.error(f"Agent failed: {e}")
    # Fall back to alternative
    result = await fallback_handler(input)
```

## Security Considerations

### API Key Management
- Environment variables for sensitive data
- No keys in source code
- Rotation support via configuration

### Input Validation
- Pydantic models for all inputs
- File type verification
- Content sanitization

### Data Privacy
- User data encrypted at rest
- Session-based data isolation
- GDPR-compliant data handling

## Scalability Considerations

### Horizontal Scaling
- Stateless agent design
- Database connection pooling
- Async I/O throughout

### Performance Optimization
- Response caching (Redis-ready)
- Lazy loading of models
- Batch processing for embeddings

## Extension Points

### Adding New Agents
1. Extend `BaseAgent`
2. Implement `think()` and `execute()`
3. Register with `OrchestratorAgent`

### Adding New Features
1. Create feature module in `src/features/`
2. Define public interface in `__init__.py`
3. Integrate with relevant agents

### Adding New Models
1. Add model config to `ModelSelector`
2. Implement any custom preprocessing
3. Update model selection logic

## Testing Strategy

```
tests/
├── unit/
│   ├── test_agents.py
│   ├── test_features.py
│   └── test_models.py
├── integration/
│   ├── test_workflows.py
│   └── test_api.py
└── e2e/
    └── test_user_flows.py
```

## Deployment

### Docker Configuration

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "src/ui/main_app.py"]
```

### Environment Variables
| Variable | Description |
|----------|-------------|
| HUGGINGFACE_API_KEY | HuggingFace API authentication |
| DATABASE_URL | Database connection string |
| LOG_LEVEL | Logging verbosity |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial architecture |

---

*This document is maintained as part of the Adaptive AI Career Architect project.*
