# TripXplo AI - Intelligent Travel Assistant

An AI-powered travel planning assistant that integrates with the TripXplo API to provide intelligent travel recommendations, package discovery, and comprehensive trip planning through a conversational interface. Built with FastAPI backend and LangGraph AI agent architecture.

## 🌟 Key Features

- **🤖 AI-Powered Conversational Agent**: Uses DeepSeek model via OpenRouter for intelligent travel conversations
- **🎯 Smart Package Matching**: Automatically matches user queries to relevant travel packages
- **💰 Real-time Pricing**: Dynamic pricing calculations with customizable parameters
- **🏨 Hotel & Activity Discovery**: Comprehensive accommodation and activity recommendations
- **🚗 Transportation Options**: Vehicle booking and transportation planning
- **📱 Responsive Chat Interface**: Modern, mobile-friendly web interface
- **🔄 RESTful API**: Complete API for travel data integration
- **🐳 Docker Support**: Containerized deployment with Docker Compose

## 🏗️ Architecture

ai-age/
├── src/                    # Core application source
│   ├── core/
│   │   └── agent.py       # LangGraph AI agent with DeepSeek integration
│   ├── services/
│   │   └── tripxplo_api.py # TripXplo API client with authentication
│   ├── models/
│   │   └── schemas.py     # Pydantic data models and validation
│   ├── utils/
│   │   └── logger.py      # Structured logging utilities
│   └── config.py          # Environment configuration management
├── tests/                  # Test suite
│   └── test_main.py       # API endpoint tests
├── scripts/               # Deployment scripts
│   ├── install.bat        # Windows dependency installer
│   └── start.bat          # Windows server launcher
├── main.py                # FastAPI application with CORS middleware
├── run.py                 # Development server runner
├── index.html             # Single-page chat application
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service orchestration
└── requirements.txt       # Python dependencies

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (3.9-slim used in Docker)
- **TripXplo API Account** (email/password credentials)
- **OpenRouter API Key** (for DeepSeek AI model access)
- **Modern Web Browser** (for frontend interface)

### Installation Methods

#### Method 1: Local Development

```bash
# Clone and navigate
git clone <repository-url>
cd ai-age

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env.local
# Edit .env.local with your credentials

# Start development server
python run.py
```

#### Method 2: Docker Deployment

```bash
# Clone repository
git clone <repository-url>
cd ai-age

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Deploy with Docker Compose
docker-compose up -d
```

#### Method 3: Windows Quick Setup

```batch
# Run installation script
scripts\install.bat

# Configure .env.local with your credentials

# Start server
scripts\start.bat
```

### Environment Configuration

Create `.env.local` (development) or `.env` (production) with:

```env
# TripXplo API Credentials
TRIPXPLO_EMAIL=your_email@example.com
TRIPXPLO_PASSWORD=your_secure_password

# OpenRouter API Key (for DeepSeek AI)
OPENROUTER_API_KEY=sk-or-v1-your-api-key

# Application Settings
DEBUG=True                    # Enable debug mode
LOG_LEVEL=INFO               # Logging verbosity
```

## 📖 Usage Guide

### Web Interface

1. **Access**: Open `http://localhost:8000` or `index.html` directly
2. **Chat**: Type natural language travel queries
3. **Examples**:
   - "Show me packages for Goa"
   - "I want to visit Kerala for 5 days"
   - "What are the best hotels in Rajasthan packages?"

### API Endpoints

#### Core Endpoints

```http
POST /query
Content-Type: application/json
{
  "question": "Show me packages for Himachal Pradesh"
}
```

#### Package Management

```http
GET /packages                           # List all packages
GET /packages/{package_id}              # Package details
GET /packages/{package_id}/pricing      # Dynamic pricing
GET /packages/{package_id}/hotels       # Available hotels
GET /packages/{package_id}/vehicles     # Transportation options
GET /packages/{package_id}/activities   # Activities and attractions
```

#### Pricing Parameters

```http
GET /packages/{id}/pricing?startDate=2024-03-15&noAdult=2&noChild=1&noRoomCount=1&noExtraAdult=0
```

## 🤖 AI Agent Architecture

### LangGraph Implementation

The AI agent uses **LangGraph** for structured conversation flow:

```python
# Agent State Management
class AgentState(BaseModel):
    messages: List[dict]

# Core Processing Node
def query_node(state: AgentState) -> AgentState:
    # 1. Extract user query
    # 2. Fetch packages from TripXplo API
    # 3. Match packages to user intent
    # 4. Generate AI response via DeepSeek
    # 5. Return formatted recommendations
```

### DeepSeek Integration

- **Model**: `deepseek/deepseek-chat` via OpenRouter
- **Features**: Natural language understanding, travel expertise
- **Fallback**: Graceful error handling with informative responses

### Package Matching Algorithm

```python
# Smart matching logic
matching_packages = [
    p for p in packages 
    if user_query_lower in p.get("packageName", "").lower()
    or user_query_lower in p.get("description", "").lower()
]
```

## 🔧 Technical Stack

### Backend Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Web Framework** | FastAPI | 0.104.1 | High-performance async API |
| **AI Framework** | LangGraph | 0.0.62 | Conversation state management |
| **AI Model** | DeepSeek Chat | Latest | Natural language processing |
| **HTTP Client** | Requests | 2.31.0 | TripXplo API integration |
| **Server** | Uvicorn | 0.24.0 | ASGI server with auto-reload |
| **Validation** | Pydantic | 2.5.0 | Data modeling and validation |

### Frontend Technologies

- **Pure HTML5/CSS3/JavaScript** (no build tools required)
- **Responsive Design** with CSS Grid and Flexbox
- **Modern Fetch API** for backend communication
- **CSS Animations** for typing indicators and interactions

### Development Tools

- **Docker & Docker Compose** for containerization
- **Pytest** for automated testing
- **Python-dotenv** for environment management
- **Structured Logging** with custom logger utilities

## 🔒 Security & Best Practices

### API Security

- **Token-based Authentication** with TripXplo API
- **Automatic Token Refresh** and caching
- **CORS Middleware** with configurable origins
- **Input Validation** with Pydantic schemas

### Environment Security

```bash
# Secure practices
.env.local          # Local development (gitignored)
.env.example        # Template (version controlled)
.env               # Production (gitignored)
```

### Error Handling

- **Graceful API Failures** with fallback responses
- **Comprehensive Logging** for debugging
- **User-friendly Error Messages** in chat interface

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_main.py -v
```

### Test Coverage

- **API Endpoint Testing** with FastAPI TestClient
- **Error Handling Validation**
- **Response Structure Verification**

## 🚀 Deployment Options

### Local Development

```bash
python run.py
# Server: http://localhost:8000
# Frontend: Open index.html
```

### Docker Production

```bash
docker-compose up -d
# Automatic restart policies
# Environment variable injection
# Port mapping: 8000:8000
```

### Manual Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Monitoring & Logging

### Log Levels

- **DEBUG**: Detailed AI model interactions
- **INFO**: API calls and user queries
- **WARNING**: Non-critical issues
- **ERROR**: API failures and exceptions

### Log Format

2024-01-15 10:30:45 - INFO - query_node received user query: Show me Goa packages
2024-01-15 10:30:46 - INFO - Fetched 25 packages from API
2024-01-15 10:30:47 - INFO - Found 3 matching packages

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Develop** with tests: `pytest tests/`
4. **Commit** changes: `git commit -m 'Add amazing feature'`
5. **Push** branch: `git push origin feature/amazing-feature`
6. **Create** Pull Request

### Code Standards

- **PEP 8** Python style guide
- **Type Hints** for all functions
- **Docstrings** for public methods
- **Error Handling** for all external API calls

## 🔮 Roadmap

### Immediate Enhancements

- [ ] **User Authentication** with JWT tokens
- [ ] **Conversation History** persistence
- [ ] **Advanced Filtering** by price, duration, location
- [ ] **Multi-language Support** for international users

### Future Features

- [ ] **Booking Integration** with payment processing
- [ ] **Mobile App** with React Native
- [ ] **Voice Interface** with speech recognition
- [ ] **Recommendation Engine** with user preferences
- [ ] **Real-time Notifications** for price changes

## 📞 Support

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **Server won't start** | Check `.env.local` credentials |
| **AI responses fail** | Verify `OPENROUTER_API_KEY` |
| **No packages returned** | Confirm TripXplo API access |
| **Frontend connection error** | Ensure backend runs on port 8000 |

### Getting Help

1. **Check Logs**: Review console output for error details
2. **Verify Environment**: Ensure all required variables are set
3. **Test API**: Use `/packages` endpoint to verify TripXplo connection
4. **Review Documentation**: Check endpoint specifications
