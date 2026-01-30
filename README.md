# 🚀 Adaptive AI Career Architect

An AI-powered platform that optimizes your professional presence through intelligent profile analysis, LinkedIn optimization, and automated portfolio generation.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🔍 Profile Intelligence Engine
- **LinkedIn Profile Analysis**: Deep analysis of your professional presence
- **Pattern Extraction**: Identify winning patterns from successful profiles
- **Market Analysis**: Real-time industry demand and trend tracking

### 🧬 Career DNA Builder
- **Resume Parsing**: Extract structured data from PDF/DOCX resumes
- **GitHub Integration**: Analyze your open-source contributions
- **Unified Profile**: Merge data from multiple sources

### ✏️ LinkedIn Optimizer
- **AI Headline Generation**: Compelling headlines with 40%+ visibility boost
- **About Section Writer**: Engaging professional summaries
- **Experience Optimizer**: Quantified, keyword-rich achievements

### 🎨 Portfolio Builder
- **React Portfolio Generation**: Modern, responsive portfolio websites
- **Multiple Layouts**: Professional, Creative, or Minimal themes
- **One-Click Export**: Download ready-to-deploy React project

### 📊 Adaptive Feedback Loop
- **Metrics Tracking**: Monitor profile views, connections, engagement
- **AI Recommendations**: Continuous optimization suggestions
- **A/B Testing**: Compare different content variations

## 🛠️ Technology Stack

- **Backend**: Python 3.9+
- **UI Framework**: Streamlit
- **AI/ML**: HuggingFace Transformers, LangChain
- **Database**: SQLAlchemy with SQLite
- **Portfolio**: React 18, Vite, Tailwind CSS

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 18+ (for portfolio generation)
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/adaptive-ai-career-architect.git
cd adaptive-ai-career-architect
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the application**
```bash
streamlit run src/ui/main_app.py
```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# HuggingFace Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2

# GitHub Integration (Optional)
GITHUB_TOKEN=your_github_token

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

## 📁 Project Structure

```
adaptive-ai-career-architect/
├── src/
│   ├── agents/              # AI Agent implementations
│   │   ├── base_agent.py
│   │   ├── orchestrator_agent.py
│   │   ├── profile_analyzer_agent.py
│   │   ├── content_generator_agent.py
│   │   ├── portfolio_agent.py
│   │   └── optimization_agent.py
│   ├── features/            # Feature modules
│   │   ├── profile_intelligence/
│   │   ├── career_dna/
│   │   ├── linkedin_optimizer/
│   │   ├── portfolio_builder/
│   │   └── feedback_loop/
│   ├── models/              # AI Model integrations
│   │   ├── huggingface_client.py
│   │   └── model_selector.py
│   ├── ui/                  # Streamlit UI
│   │   ├── main_app.py
│   │   └── components/
│   ├── database/            # Data persistence
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── repositories.py
│   ├── utils/               # Utilities
│   │   ├── logger.py
│   │   └── helpers.py
│   └── config/              # Configuration
│       └── settings.py
├── templates/               # Portfolio templates
│   └── portfolio/
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Usage

### 1. Profile Input
Upload your resume, enter LinkedIn URL, or manually input your information.

### 2. Career DNA Analysis
The system analyzes your profile and generates a comprehensive Career DNA including:
- Professional archetype
- Core strengths
- Skills breakdown
- Career trajectory
- Market fit analysis

### 3. LinkedIn Optimization
Receive AI-generated suggestions for:
- Headlines (with visibility scores)
- About section (with improvement highlights)
- Experience descriptions (with keywords)

### 4. Portfolio Generation
Generate a complete React portfolio website:
- Choose from multiple layouts
- Customize color schemes
- Download ready-to-deploy project

## 🔧 API Reference

### HuggingFace Client

```python
from src.models import HuggingFaceClient

client = HuggingFaceClient()

# Text Generation
response = await client.generate("Write a professional headline")

# Embeddings
embeddings = await client.embed_text("Your text here")

# Classification
labels = await client.classify("Text", ["Category A", "Category B"])
```

### Agents

```python
from src.agents import OrchestratorAgent

orchestrator = OrchestratorAgent()
results = await orchestrator.run({
    "workflow": "full_optimization",
    "profile_data": {...}
})
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_agents.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) for AI models
- [Streamlit](https://streamlit.io/) for the UI framework
- [LangChain](https://langchain.com/) for agent orchestration

## 📧 Contact

For questions or feedback, please open an issue or reach out to the maintainers.

---

**Built with ❤️ using AI-powered tools**
