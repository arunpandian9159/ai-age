# TripXplo AI Frontend

A simple, single-page chat interface for the TripXplo AI travel assistant.

## Features

- Clean, modern chat interface
- Real-time messaging with the AI backend
- Responsive design for mobile and desktop
- Typing indicators and loading states
- Error handling for connection issues

## Setup

1. Make sure your backend server is running on `http://localhost:8000`
2. Open `index.html` in your web browser
3. Start chatting with the AI travel assistant!

## Usage

Simply type your travel-related questions in the chat input and press Enter or click Send. The AI will help you with:

- Travel package recommendations
- Destination information
- Hotel suggestions
- Activity recommendations
- Pricing information
- And much more!

## Backend Connection

The frontend connects to the FastAPI backend running on `http://localhost:8000`. If your backend runs on a different port, update the `apiUrl` variable in the JavaScript section of `index.html`.

## Browser Compatibility

This frontend works in all modern browsers including:
- Chrome
- Firefox
- Safari
- Edge

No additional dependencies or build tools required!