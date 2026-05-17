import React, { useState } from 'react';
import { aiService, analyticsService } from '../../services/api';
import toast from 'react-hot-toast';
import { Send, Bot, Sparkles, TrendingUp } from 'lucide-react';

const AIAssistant = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);

  const questionCategories = {
    "Peak Time Analysis": [
      "What is the peak hour for sales?",
      "Which hours have the highest orders?",
      "What time does Tea sell the most?",
      "When is the busiest time of the day?",
      "Show me hourly sales patterns",
    ],
    "Peak Day Analysis": [
      "What day has the highest sales?",
      "Which day sells the most Veg Puff?",
      "What are the busiest days of the week?",
      "Compare Monday vs Friday sales",
      "Which weekday has lowest sales?",
    ],
    "Top Items & Revenue": [
      "What are the top 5 selling items?",
      "Which item generates most revenue?",
      "What food sells the most on Monday?",
      "Show me best performing items",
      "Which category makes most money?",
    ],
    "Waste & Inventory": [
      "Which item causes the most wastage?",
      "What items am I over-preparing?",
      "Show me food waste analysis",
      "Which items have low demand?",
      "How can I reduce waste?",
    ],
    "Predictions & Planning": [
      "What should I prepare tomorrow?",
      "Recommend breakfast quantities for Monday",
      "Predict demand for next week",
      "What items should I stock more?",
      "Give me preparation suggestions",
    ],
    "Weekly Insights": [
      "Give me this week sales summary",
      "Compare this week vs last week",
      "Which day performed best this week?",
      "Show week over week growth",
      "What should I improve next week?",
    ],
    "Monthly Insights": [
      "Show me monthly performance summary",
      "What is total revenue this month?",
      "Which day is strongest in this month?",
      "How is monthly average daily sales?",
      "Give me monthly planning recommendations",
    ],
    "Category & Meal-Time Insights": [
      "Which breakfast items perform best?",
      "What sells most during lunch time?",
      "Which snacks have highest demand?",
      "How does dinner sales perform?",
      "Suggest meal-wise stock strategy",
    ],
    "Operations & Staffing": [
      "When should I add more staff?",
      "What are my slow hours for staff breaks?",
      "Which days need extra inventory?",
      "What time should I start preparing food?",
      "Give me operations optimization tips",
    ],
    "Custom Deep-Dive Questions": [
      "What are my biggest business risks right now?",
      "Which 3 items need immediate action?",
      "How can I improve profit with current menu?",
      "What promotions should I run this week?",
      "Give me a complete action plan for tomorrow",
    ],
  };

  const handleAskQuestion = async (questionText = query) => {
    if (!questionText.trim()) {
      toast.error('Please enter a question');
      return;
    }

    setLoading(true);
    try {
      const res = await aiService.query(questionText);
      setResponse(res.data.response);
      setQuery('');
    } catch (error) {
      toast.error('Failed to get AI response');
    } finally {
      setLoading(false);
    }
  };

  const handleGetPredictions = async () => {
    setLoading(true);
    try {
      const res = await analyticsService.getPredictions();
      setPredictions(res.data);
      setResponse('Here are the demand predictions for tomorrow:');
    } catch (error) {
      toast.error('Failed to get predictions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center space-x-3">
          <Bot className="h-8 w-8 text-primary-500" />
          <span>AI Assistant</span>
        </h1>
        <p className="text-gray-600">Ask questions about your canteen analytics and get insights</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Question Input */}
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="text-xl font-bold mb-4 flex items-center space-x-2">
              <Sparkles className="h-5 w-5 text-primary-500" />
              <span>Ask a Question</span>
            </h2>

            <div className="flex space-x-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                placeholder="Ask me anything about your canteen..."
                className="input-field flex-1"
              />
              <button
                onClick={() => handleAskQuestion()}
                disabled={loading}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                <Send className="h-5 w-5" />
                <span>Ask</span>
              </button>
            </div>

            {/* Suggested Questions by Category */}
            <div className="mt-6">
              <p className="text-sm font-semibold text-gray-700 mb-3">💡 Chat Sections (tap any question):</p>
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {Object.entries(questionCategories).map(([category, questions]) => (
                  <div key={category} className="p-3 rounded-xl border border-primary-100 bg-white">
                    <p className="text-xs font-bold text-primary-700 mb-2 tracking-wide uppercase">{category}</p>
                    <div className="flex flex-wrap gap-2">
                      {questions.map((q, index) => (
                        <button
                          key={index}
                          onClick={() => handleAskQuestion(q)}
                          disabled={loading}
                          className="px-3 py-1.5 text-xs bg-gradient-to-r from-primary-50 to-primary-100 hover:from-primary-100 hover:to-primary-200 text-primary-700 rounded-full transition shadow-sm hover:shadow disabled:opacity-50"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Response */}
          {response && (
            <div className="card bg-gradient-to-br from-primary-50 to-white border-2 border-primary-200">
              <div className="flex items-start space-x-3">
                <Bot className="h-6 w-6 text-primary-600 flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 mb-2">AI Response:</h3>
                  <div className="text-gray-700 whitespace-pre-line">{response}</div>
                </div>
              </div>
            </div>
          )}

          {/* Predictions */}
          {predictions.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-bold mb-4 flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-500" />
                <span>Tomorrow's Demand Forecast</span>
              </h3>
              <div className="space-y-3">
                {predictions.map(pred => (
                  <div key={pred.item_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{pred.item_name}</p>
                      <p className="text-sm text-gray-600">
                        Confidence: {(pred.confidence * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-primary-600">{pred.predicted_quantity}</p>
                      <p className="text-xs text-gray-600">units</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="space-y-4">
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
            
            <button
              onClick={handleGetPredictions}
              disabled={loading}
              className="w-full btn-primary mb-3 flex items-center justify-center space-x-2"
            >
              <TrendingUp className="h-5 w-5" />
              <span>Get Predictions</span>
            </button>

            <div className="space-y-2 text-sm text-gray-600">
              <div className="p-3 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900">💡 Tip</p>
                <p className="text-blue-700 mt-1">
                  Ask specific questions to get better insights
                </p>
              </div>

              <div className="p-3 bg-green-50 rounded-lg">
                <p className="font-semibold text-green-900">🎯 Example</p>
                <p className="text-green-700 mt-1">
                  "What items sell best during lunch hours?"
                </p>
              </div>
            </div>
          </div>

          <div className="card bg-gradient-to-br from-purple-50 to-white">
            <h3 className="font-bold text-purple-900 mb-2">How it works</h3>
            <ul className="text-sm text-purple-700 space-y-1">
              <li>• Analyzes historical sales data</li>
              <li>• Identifies patterns and trends</li>
              <li>• Provides actionable insights</li>
              <li>• Predicts future demand</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
