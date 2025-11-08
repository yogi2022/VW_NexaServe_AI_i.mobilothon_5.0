# VW NexaServe AI - Requirements and Installation Guide

## Requirements File (requirements.txt)

```txt
streamlit>=1.28.0
openai>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
Pillow>=10.0.0
python-dateutil>=2.8.2
```

## Installation Instructions

### Step 1: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run vw-nexaserve-ai.py
```

The application will open in your browser at `http://localhost:8501`

## Features Implemented

### ✅ Complete Feature Set

1. **Multimodal AI Interface**
   - Text-based chat with GPT-4 integration
   - Image upload and analysis
   - Voice input simulation
   - Real-time conversation history

2. **Emotional Intelligence**
   - Real-time sentiment analysis
   - Frustration score tracking
   - Automatic escalation triggers
   - Sentiment analytics dashboard

3. **Digital Twin Dashboard**
   - Real-time vehicle health monitoring
   - Component health visualization
   - Predictive maintenance alerts
   - Interactive health metrics

4. **Blockchain Service Ledger**
   - Immutable service records
   - SHA-256 hash verification
   - Complete service history tracking
   - Blockchain-verified timestamps

5. **AR Remote Assistance**
   - AR session simulation
   - Expert assignment
   - Live session management
   - AR annotation features

6. **Smart Appointment Booking**
   - AI-powered slot optimization
   - Multi-location support
   - Automatic parts verification
   - Cost estimation

7. **Customer Authentication**
   - Secure login system
   - Session management
   - User vehicle linking

## Architecture Overview

### Layer 1: User Interface
- Streamlit web application
- Responsive design with custom CSS
- Multi-page navigation
- Interactive dashboards

### Layer 2: AI Engine
- OpenAI GPT-4 integration
- Sentiment analysis
- Issue classification
- Response generation

### Layer 3: Data Management
- Session state persistence
- Digital twin data simulation
- Service record management
- Real-time analytics

### Layer 4: Visualization
- Plotly interactive charts
- Component health gauges
- Sentiment timeline graphs
- Service history display

## API Configuration

**Important:** The OpenAI API key is embedded in the code. For production deployment:

1. Move API key to environment variables:
```python
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_actual_key_here
```

3. Add python-dotenv to requirements:
```bash
pip install python-dotenv
```

4. Load in code:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Usage Guide

### 1. Login
- Enter your name
- Provide vehicle registration number
- Click "Login"

### 2. Chat Interface
- Use text input for questions
- Upload images for visual diagnosis
- Try voice simulation
- Click quick action buttons

### 3. Digital Twin Dashboard
- View overall vehicle health
- Check component status
- Review predictive alerts
- Monitor tire health

### 4. Book Appointment
- Select service type
- Choose preferred date
- Get AI-optimized slot
- Receive blockchain confirmation

### 5. AR Assistance
- Start AR session
- Connect with expert
- View AR annotations
- End session when resolved

## Technology Stack

- **Frontend Framework:** Streamlit 1.28+
- **AI/ML:** OpenAI GPT-4 Turbo
- **Data Visualization:** Plotly, Pandas
- **Image Processing:** PIL (Pillow)
- **Backend Logic:** Python 3.8+
- **State Management:** Streamlit Session State
- **Security:** SHA-256 Hashing

## Performance Optimizations

1. **Session State Caching**
   - Persistent user data across reruns
   - Efficient message history management

2. **Lazy Loading**
   - Components load only when needed
   - Reduced initial page load time

3. **Efficient Rendering**
   - Minimal re-renders with st.rerun()
   - Optimized chart updates

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Automatic HTTPS and scaling

### Option 2: Local Server
```bash
streamlit run vw-nexaserve-ai.py --server.port 8501
```

### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY vw-nexaserve-ai.py .
EXPOSE 8501
CMD ["streamlit", "run", "vw-nexaserve-ai.py"]
```

## Troubleshooting

### Issue: OpenAI API Error
**Solution:** Verify API key is valid and has sufficient credits

### Issue: Import Errors
**Solution:** Ensure all dependencies installed: `pip install -r requirements.txt`

### Issue: Session State Reset
**Solution:** This is expected on browser refresh - data persists within session

### Issue: Plotly Charts Not Rendering
**Solution:** Update plotly: `pip install --upgrade plotly`

## Future Enhancements

1. **Integration with Real APIs**
   - VW service center APIs
   - Real-time vehicle telemetry
   - Actual blockchain integration

2. **Advanced Features**
   - WebRTC for real AR streaming
   - Multi-language support (i18n)
   - Database persistence (PostgreSQL/MongoDB)
   - Real voice input (Whisper API)

3. **Mobile App**
   - React Native companion app
   - Push notifications
   - Offline mode support

## Security Considerations

- API keys should be environment variables
- Implement user authentication with OAuth
- Add rate limiting for API calls
- Enable HTTPS in production
- Sanitize user inputs
- Add CSRF protection

## Contact & Support

For hackathon queries or technical issues:
- Review code comments for detailed explanations
- Check Streamlit documentation: https://docs.streamlit.io
- OpenAI API docs: https://platform.openai.com/docs

## License

Developed for i.mobilothon 5.0 - Volkswagen Hackathon

---

**Built with innovation for Volkswagen's Future of Mobility** 🚗✨
