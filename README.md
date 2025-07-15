# TripXplo AI — Intelligent Travel Assistant

TripXplo AI is an AI-powered travel planning assistant that integrates with the TripXplo API to provide intelligent travel recommendations, package discovery, and trip planning through a conversational interface. The backend is built with FastAPI and uses LangGraph for AI agent state management, leveraging the DeepSeek model via OpenRouter.

## Features
- Conversational AI for travel planning
- Smart matching of user queries to travel packages
- Real-time pricing, hotel, vehicle, and activity discovery
- RESTful API endpoints for integration
- Responsive web chat interface (HTML/JS, no build tools required)
- Docker and Windows support for easy deployment

## API Endpoints
- `GET /` — Welcome message
- `POST /query` — Main conversational endpoint (expects `{ "question": "..." }`)
- `GET /packages` — List all travel packages
- `GET /packages/{package_id}` — Get details for a specific package
- `GET /packages/{package_id}/pricing` — Get dynamic pricing for a package
- `GET /packages/{package_id}/vehicles` — List available vehicles for a package
- `GET /packages/{package_id}/activities` — List activities for a package

## AI Agent Architecture
- User queries are processed by a LangGraph-based agent
- The agent fetches packages from TripXplo, matches them to the query, and generates a response using DeepSeek
- The agent is stateful and can handle multi-turn conversations

## Environment & Configuration
Create a `.env.local` (for development) or `.env` (for production) file with the following variables:

```
TRIPXPLO_EMAIL=your_email@example.com
TRIPXPLO_PASSWORD=your_tripxplo_password
OPENROUTER_API_KEY=your_openrouter_api_key
DEBUG=True
LOG_LEVEL=INFO
```

## Installation & Running

### Local Development
```bash
pip install -r requirements.txt
# Configure .env.local with your credentials
python run.py
```

### Docker
```bash
# Configure .env with your credentials
# Then run:
docker-compose up -d
```

### Windows (Batch Scripts)
```batch
scripts\install.bat
# Configure .env.local
scripts\start.bat
```

## Web Interface
Open `index.html` in your browser and connect to the backend at `http://localhost:8000`.

## Testing
Run all tests with:
```bash
pytest
```

## License
MIT
