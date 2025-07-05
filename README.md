# Synthetic_query_generator_uisng_llm
A systme which mimics the generation of user queries and automates conversation chain between user and bot (both llm)

🤖 AI Conversation Flow Tester
A comprehensive Streamlit application for generating and analyzing multi-turn conversations for train/bus ticket services. This tool helps test AI assistant responses across various customer service scenarios with automated flow generation and escalation detection.

📋 Features
🚀 Core Functionality
Multi-turn Conversation Generation: Automatically generates realistic conversation flows up to 15 turns
Predefined Flow Types: Built-in templates for common customer service scenarios
Custom Query Support: Create custom conversation flows with your own initial queries
Real-time Processing: Live conversation generation with progress tracking
Escalation Detection: Automatic detection of when cases should be escalated to human agents

*🎯 Supported Service Domains*
    Ticket Cancellation: Full and partial cancellation workflows
    Ticket Details: Status checks and booking confirmation requests
    Ticket Rescheduling: Date/time changes and alternate booking options
    Bus/Train Information: Live tracking and service details
    Refund Processing: Payment issues and refund status tracking
    Case Updates: Complaint status and resolution tracking

**📊 Analytics & Export**
    Real-time Statistics: Turn count, escalation rates, and flow metrics
    Export Options: Download conversations as CSV or JSON
    Visual Progress Tracking: Live progress indicators during generation
    Conversation History: Detailed turn-by-turn analysis with metadata

**🛠 Installation**
Prerequisites
Python 3.8+
Streamlit
Required Python packages (see requirements below)

Setup
Clone the repository
"""
git clone https://github.com/your-username/ai-conversation-flow-tester.git
cd ai-conversation-flow-tester
"""
**Create virtual environment**
python -m venv streamvenv
source streamvenv/bin/activate  # On Windows: streamvenv\Scripts\activate

Install dependencies
pip install streamlit requests pandas

Run the application
streamlit run app.py

🔧 Configuration
API Endpoints
The application uses two main API endpoints:

Query Generation: http://gir.redbus.com/openai4/chat/completions
Assistant Response: http://selfhelp-gpt.redbus.com:17714/chat/query
Environment Variables
Create a .env file for secure credential management:

LLM_USERNAME=your_username
LLM_PASSWORD=your_password
API_TIMEOUT=30

🚀 Usage
    Starting a Conversation Flow
    Select Flow Type: Choose from predefined scenarios or create custom queries
    Configure Depth: Set maximum conversation turns (1-15)
    Start Flow: Click "Start Predefined Flow" or "Start Custom Flow"
    Monitor Progress: Watch real-time conversation generation
    Export Results: Download as CSV or JSON when complete

Predefined Flow Options

Flow Type	Initial Query	Use Case
Ticket Cancellation	"I want to cancel this ticket, can i cancel this"	Test cancellation workflows
Ticket Details	"what is the latest status of my Tin"	Verify information retrieval
Ticket Reschedule	"I want to reschedule my ticket"	Test rescheduling logic
Bus/Train Information	"where is my bus right now"	Live tracking scenarios
Refund Details	"My payment was debited twice"	Payment issue handling
Train/Bus Details	"what is my coach position"	Detailed service information
Case Updates Query	"what is the status of my complaint"	Complaint tracking

Custom Queries
Create your own conversation starters by:

Selecting "Custom Query" in the sidebar
Entering your query in the text area
Clicking "Start Custom Flow"

📊 Understanding Results
Conversation Metrics
    Total Turns: Number of conversation exchanges
    Case Creations: Instances where escalation to human agents occurred
    Escalation Rate: Percentage of turns requiring human intervention

Turn Analysis
Each conversation turn includes:

User Query: The generated or initial user input
    Assistant Response: AI assistant's reply
    Case Creation Flag: Whether escalation was triggered
    Timestamp: When the turn was processed
    Node ID: Unique identifier for tracking


Export Formats
CSV Export
timestamp,depth,node_id,case_creation,user_query,assistant_response
2024-01-15T10:30:00,0,A1B2C3D4,false,"I want to cancel my ticket","I'll help you with..."

JSON Export
{
  "timestamp": "2024-01-15T10:30:00",
  "depth": 0,
  "node_id": "A1B2C3D4",
  "case_creation": false,
  "user_query": "I want to cancel my ticket",
  "assistant_response": "I'll help you with..."
}

🔍 Flow Evaluation Logic
The system evaluates conversations based on:

✅ Valid Flow Indicators
    Follows expected service-specific sequences
    Provides appropriate escalation paths
    Acknowledges user concerns properly
    Maintains task continuity

🚨 Escalation Triggers
    User dissatisfaction with responses
    Legal or social media threats
    Post-journey complaints
    Multiple payment issues
    Service failures (delayed/cancelled buses)

🛡 Error Handling
Common Issues & Solutions
    Issue	Cause	Solution
    API Timeout	Network connectivity	Check internet connection, verify API endpoints
    JSON Parse Error	Malformed response	Retry generation, check API response format
    Flow Termination	No follow-up queries	Review conversation context, manually continue
    Authentication Error	Invalid credentials	Update username/password in configuration

Fallback Mechanisms
    Default queries when generation fails
    Graceful degradation for API issues
    Automatic retry logic for network errors

📁 File Structure
ai-conversation-flow-tester/
├── app.py                          # Main Streamlit application
├── streamvenv/                     # Virtual environment
├── streamlit_conversation.csv      # Generated conversation data (CSV)
├── streamlit_conversation.json     # Generated conversation data (JSON)
├── README.md                       # This file
└── requirements.txt               # Python dependencies


🤝 Contributing
    Development Setup
    Fork the repository
    Create a feature branch: git checkout -b feature-name
    Make your changes
    Test thoroughly
    Submit a pull request

Code Style
    Follow PEP 8 guidelines
    Add docstrings for functions
    Include error handling
    Write descriptive commit messages

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🐛 Troubleshooting
Performance Issues
    Reduce max conversation depth
    Check network connectivity
    Monitor API response times

Data Export Problems
    Ensure conversation data exists before export
    Check file permissions
    Verify disk space

Flow Generation Issues
    Validate initial query format
    Check API credentials
    Review conversation context

📞 Support
For issues and questions:

    Check the troubleshooting section
    Review existing GitHub issues
    Create a new issue with detailed description
    Include error logs and reproduction steps

🔄 Updates & Roadmap

Recent Changes

    Added real-time progress tracking
    Improved error handling
    Enhanced export functionality
    Added custom query support
Future Enhancements
    Multi-language support
    Advanced analytics dashboard
    Integration with more APIs
    Batch processing capabilities
    A/B testing framework
Made with ❤️ for better customer service AI testing
