import { useState } from "react";
import { MapPin, Send, Sparkles, Loader2, Compass, Mountain, Camera, Coffee } from "lucide-react";

interface Suggestion {
  icon: React.ComponentType<{ className?: string }>;
  text: string;
  color: string;
}

const TravelIndiaApp = () => {
  const [question, setQuestion] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const askAgent = async (): Promise<void> => {
    if (!question.trim()) return;
    
    setLoading(true);
    setResponse("");

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setResponse(data.response);
    } catch (err) {
      console.error("API error:", err);
      setResponse("Oops! Something went wrong. Please try again.");
    }

    setLoading(false);
  };
  
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === "Enter" && !loading) {
      askAgent();
    }
  };
  
  const suggestions: Suggestion[] = [
    { icon: Mountain, text: "Best hill stations in Kerala", color: "from-green-500 to-emerald-600" },
    { icon: Camera, text: "Hidden gems in Rajasthan", color: "from-purple-500 to-pink-600" },
    { icon: Coffee, text: "Street food tour in Mumbai", color: "from-orange-500 to-red-600" },
    { icon: Compass, text: "Backpacking routes in Himachal", color: "from-blue-500 to-indigo-600" }
  ];

  return (
    <div className="min-h-screen bg-animated-gradient">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-orange-200/30 to-red-200/30 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-blue-200/30 to-purple-200/30 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Header */}
      <header className="relative glass-header sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl blur opacity-75"></div>
                <div className="icon-container-primary">
                  <MapPin className="w-8 h-8 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text-primary">
                  Travel India AI
                </h1>
                <p className="text-gray-600 font-medium">Discover incredible destinations across India</p>
              </div>
            </div>
            <div className="hidden md:flex badge-secondary">
              <Sparkles className="w-4 h-4 text-orange-600" />
              <span className="text-sm font-semibold text-orange-700">AI-Powered</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16 animate-fade-in">
          <div className="badge-primary mb-8">
            <Sparkles className="w-5 h-5" />
            Your Personal Travel Assistant
          </div>
          <h2 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6 leading-tight">
            Where would you like to
            <span className="block gradient-text-primary">
              explore today?
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Ask me about the best places to visit, hidden gems, cultural experiences, 
            food recommendations, and travel tips for anywhere in incredible India.
          </p>
        </div>

        {/* Search Section */}
        <div className="glass-container rounded-3xl p-8 mb-12 animate-slide-up">
          <div className="flex flex-col lg:flex-row gap-6">
            <div className="flex-1 relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-orange-400/30 to-red-400/30 rounded-2xl blur-sm opacity-0 group-focus-within:opacity-100 transition-all duration-500"></div>
              <input
                type="text"
                placeholder="Ask about places to visit in India..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                className="input-primary relative"
              />
              {question && (
                <button
                  onClick={() => setQuestion("")}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 w-8 h-8 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-all duration-200"
                >
                  ×
                </button>
              )}
            </div>
            <button
              onClick={askAgent}
              disabled={loading || !question.trim()}
              className="btn-primary flex items-center gap-3 min-w-[180px] justify-center"
            >
              {loading ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  Thinking...
                </>
              ) : (
                <>
                  <Send className="w-6 h-6" />
                  Ask Agent
                </>
              )}
            </button>
          </div>
        </div>

        {/* Response Section */}
        {(response || loading) && (
          <div className="glass-container rounded-3xl border-green-200/30 p-8 mb-12 animate-slide-up">
            <div className="flex items-center gap-4 mb-8">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl blur-sm opacity-75"></div>
                <div className="icon-container-secondary">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-800">AI Response</h3>
            </div>
            
            {loading ? (
              <div className="flex items-center justify-center py-16">
                <div className="text-center">
                  <div className="relative mb-6">
                    <div className="loading-spinner mx-auto"></div>
                    <div className="loading-ping mx-auto"></div>
                  </div>
                  <p className="text-xl text-gray-600 font-medium">Exploring the best recommendations for you...</p>
                  <p className="text-gray-500 mt-2">This may take a few moments</p>
                </div>
              </div>
            ) : (
              <div className="prose prose-xl max-w-none">
                <div className="response-container">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap text-lg font-medium">{response}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Suggestions */}
        {!response && !loading && (
          <div className="animate-fade-in">
            <h3 className="text-3xl font-bold text-gray-800 text-center mb-12">
              <span className="gradient-text-primary">
                Popular Questions
              </span>
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              {suggestions.map((suggestion, index) => {
                const IconComponent = suggestion.icon;
                return (
                  <button
                    key={index}
                    onClick={() => setQuestion(suggestion.text)}
                    className="suggestion-card"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="flex items-center gap-4">
                      <div className={`p-4 bg-gradient-to-r ${suggestion.color} rounded-xl group-hover:scale-125 group-hover:rotate-3 transition-all duration-500 shadow-xl`}>
                        <IconComponent className="w-6 h-6 text-white" />
                      </div>
                      <span className="text-gray-700 group-hover:text-gray-900 transition-colors font-semibold text-xl">
                        {suggestion.text}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative glass-header border-t border-orange-200/50 mt-20">
        <div className="max-w-6xl mx-auto px-6 py-12 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-orange-500" />
            <p className="text-gray-700 font-bold text-lg">Powered by AI</p>
          </div>
          <p className="text-gray-600 text-lg">
            Discover the incredible diversity and beauty of India with intelligent travel recommendations
          </p>
        </div>
      </footer>
    </div>
  );
};

export default TravelIndiaApp;
