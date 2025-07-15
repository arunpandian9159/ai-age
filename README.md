# TripXplo AI - Travel Assistant

A comprehensive AI-powered travel assistant that helps users discover travel packages, get destination information, and plan their trips. The application consists of a FastAPI backend with AI agent capabilities and a simple, responsive frontend interface.

## 🌟 Features

- **AI-Powered Travel Assistant**: Intelligent conversational agent for travel planning
- **Travel Package Discovery**: Browse and search travel packages
- **Real-time Pricing**: Get up-to-date pricing information for packages
- **Hotel & Activity Recommendations**: Discover accommodations and activities
- **Vehicle Options**: Find transportation options for your trip
- **Responsive Web Interface**: Clean, modern chat interface that works on all devices
- **RESTful API**: Comprehensive API for travel data and AI interactions

## 🏗️ Architecture

```
ai-age/
├── backend/           # FastAPI backend with AI agent
│   ├── main.py       # Main FastAPI application
│   ├── agent.py      # AI agent implementation
│   ├── tripxplo_api.py # Travel API integration
│   └── api/          # API endpoints
├── frontend/         # Simple HTML/CSS/JS frontend
│   └── index.html    # Single-page chat interface
└── requirements.txt  # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Modern web browser
- OpenAI API key (for AI functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-age
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Start the backend server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open the frontend**
   Open `frontend/index.html` in your web browser

## 📖 Usage

### Web Interface
1. Open the frontend in your browser
2. Type your travel-related questions in the chat interface
3. Get AI-powered recommendations and information

### API Endpoints

The backend provides several REST endpoints:

- `POST /query` - Chat with the AI travel assistant
- `GET /packages` - Get all available travel packages
- `GET /packages/{id}` - Get specific package details
- `GET /packages/{id}/pricing` - Get package pricing
- `GET /packages/{id}/hotels` - Get available hotels
- `GET /packages/{id}/vehicles` - Get available vehicles
- `GET /packages/{id}/activities` - Get available activities

## 🛠️ Development

### Backend Development
See [backend/README.md](backend/README.md) for detailed backend documentation.

### Frontend Development
See [frontend/README.md](frontend/README.md) for frontend-specific information.

### Running in Development Mode

1. **Backend** (with auto-reload):
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Frontend**: Simply open `frontend/index.html` in your browser

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI functionality | Yes |

### API Configuration

The frontend is configured to connect to `http://localhost:8000` by default. To change this, update the `apiUrl` variable in `frontend/index.html`.

## 📦 Dependencies

### Backend
- FastAPI - Modern web framework for APIs
- OpenAI - AI integration
- Uvicorn - ASGI server
- Pydantic - Data validation
- HTTPX - HTTP client
- Supabase - Database integration
- Python-dotenv - Environment variable management

### Frontend
- Pure HTML/CSS/JavaScript (no build tools required)
- Modern browser APIs for fetch and DOM manipulation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the documentation in the respective README files
2. Review the API endpoints and their expected parameters
3. Ensure all environment variables are properly set
4. Verify that the backend server is running before using the frontend

## 🔮 Future Enhancements

- User authentication and personalized recommendations
- Booking integration
- Multi-language support
- Mobile app development
- Advanced filtering and search capabilities
- Integration with more travel APIs