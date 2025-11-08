# VW NexaServe AI - Multimodal Intelligent After-Sales Ecosystem
# "Where Every Customer Conversation Becomes a Service Revolution"
# Complete Streamlit Implementation for i.mobilothon 5.0

import streamlit as st
import openai
from openai import OpenAI
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import uuid
from PIL import Image
import io
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ================================
# CONFIGURATION & INITIALIZATION
# ================================

# Page Configuration
st.set_page_config(
    page_title="VW NexaServe AI - After-Sales Revolution",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Styling
st.markdown("""
<style>
    /* Main Theme */
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 10px 0;
        color: white;
    }
    
    .service-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
    }
    
    .sub-header {
        font-size: 24px;
        color: #667eea;
        font-weight: 600;
        margin: 20px 0;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    
    /* Chat Interface */
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: slideIn 0.3s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f7f7f7;
        color: #333;
        margin-right: 20%;
        border-left: 4px solid #667eea;
    }
    
    /* Emotion Indicators */
    .emotion-positive {
        color: #10b981;
        font-weight: bold;
    }
    
    .emotion-neutral {
        color: #f59e0b;
        font-weight: bold;
    }
    
    .emotion-negative {
        color: #ef4444;
        font-weight: bold;
        animation: pulse 1s infinite;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 5px;
    }
    
    .status-active {
        background: #10b981;
        color: white;
    }
    
    .status-pending {
        background: #f59e0b;
        color: white;
    }
    
    .status-completed {
        background: #3b82f6;
        color: white;
    }
    
    /* Blockchain Badge */
    .blockchain-verified {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        padding: 5px 10px;
        border-radius: 5px;
        color: #000;
        font-weight: bold;
        display: inline-block;
    }
    
    /* AR Indicator */
    .ar-active {
        background: #8b5cf6;
        color: white;
        padding: 10px;
        border-radius: 8px;
        animation: pulse 2s infinite;
    }
    
    /* Sidebar Enhancement */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ================================
# OPENAI CLIENT INITIALIZATION
# ================================

# Initialize OpenAI Client with provided API key
# OPENAI_API_KEY = "Enter your API Key"
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"⚠️ OpenAI Client Initialization Error: {e}")

# ================================
# SESSION STATE INITIALIZATION
# ================================

def initialize_session_state():
    """Initialize all session state variables"""
    
    # User Session
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'user_vehicle_id' not in st.session_state:
        st.session_state.user_vehicle_id = ""
    
    # Chat History
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sentiment Tracking
    if 'sentiment_history' not in st.session_state:
        st.session_state.sentiment_history = []
    
    if 'current_sentiment' not in st.session_state:
        st.session_state.current_sentiment = "neutral"
    
    if 'frustration_score' not in st.session_state:
        st.session_state.frustration_score = 0
    
    # Service Records (Blockchain Simulation)
    if 'service_records' not in st.session_state:
        st.session_state.service_records = []
    
    # Digital Twin Data
    if 'digital_twin_data' not in st.session_state:
        st.session_state.digital_twin_data = generate_digital_twin_data()
    
    # AR Session
    if 'ar_session_active' not in st.session_state:
        st.session_state.ar_session_active = False
    
    # Issue Classification
    if 'current_issue' not in st.session_state:
        st.session_state.current_issue = None
    
    # Service Appointment
    if 'appointment_scheduled' not in st.session_state:
        st.session_state.appointment_scheduled = False
    
    if 'ar_session_data' not in st.session_state:
        st.session_state.ar_session_data = None

# ================================
# DIGITAL TWIN SIMULATION
# ================================

def generate_digital_twin_data():
    """Generate realistic digital twin data for vehicle"""
    return {
        'vehicle_id': 'VW-' + str(uuid.uuid4())[:8].upper(),
        'model': 'Volkswagen Taigun Highline',
        'year': 2023,
        'mileage': np.random.randint(5000, 25000),
        'last_service': (datetime.now() - timedelta(days=np.random.randint(30, 180))).strftime('%Y-%m-%d'),
        'next_service_due': (datetime.now() + timedelta(days=np.random.randint(10, 90))).strftime('%Y-%m-%d'),
        'health_score': np.random.randint(75, 98),
        'components': {
            'engine': {
                'health': np.random.randint(85, 100),
                'temperature': np.random.randint(85, 95),
                'oil_level': np.random.randint(70, 100),
                'next_oil_change': np.random.randint(1000, 5000)
            },
            'brakes': {
                'front_pad_wear': np.random.randint(20, 60),
                'rear_pad_wear': np.random.randint(25, 55),
                'fluid_level': np.random.randint(80, 100),
                'health': np.random.randint(75, 95)
            },
            'transmission': {
                'health': np.random.randint(85, 98),
                'fluid_condition': 'Good',
                'performance': np.random.randint(90, 100)
            },
            'battery': {
                'voltage': round(np.random.uniform(12.4, 12.8), 2),
                'health': np.random.randint(80, 100),
                'estimated_life': np.random.randint(12, 36)
            },
            'tires': {
                'front_left': np.random.randint(60, 95),
                'front_right': np.random.randint(60, 95),
                'rear_left': np.random.randint(65, 95),
                'rear_right': np.random.randint(65, 95),
                'pressure_status': 'Optimal'
            },
            'suspension': {
                'health': np.random.randint(75, 95),
                'shock_absorbers': 'Good'
            }
        },
        'predictive_alerts': []
    }

def update_digital_twin_predictions(twin_data):
    """Generate predictive maintenance alerts"""
    alerts = []
    
    # Engine oil change prediction
    if twin_data['components']['engine']['next_oil_change'] < 2000:
        alerts.append({
            'severity': 'Medium',
            'component': 'Engine Oil',
            'message': f"Oil change recommended in {twin_data['components']['engine']['next_oil_change']} km",
            'predicted_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        })
    
    # Brake pad wear prediction
    if twin_data['components']['brakes']['front_pad_wear'] > 50:
        alerts.append({
            'severity': 'High',
            'component': 'Brake Pads',
            'message': 'Front brake pads showing significant wear ({}%)'.format(twin_data['components']['brakes']['front_pad_wear']),
            'predicted_date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d')
        })
    
    # Battery health prediction
    if twin_data['components']['battery']['health'] < 85:
        alerts.append({
            'severity': 'Medium',
            'component': 'Battery',
            'message': f"Battery health at {twin_data['components']['battery']['health']}%. Consider replacement soon.",
            'predicted_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        })
    
    twin_data['predictive_alerts'] = alerts
    return twin_data

# ================================
# SENTIMENT ANALYSIS
# ================================

def analyze_sentiment(text):
    """Analyze sentiment and emotion from user input using GPT-4"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an emotional intelligence AI specialized in analyzing customer sentiment in automotive service contexts. 
                    Analyze the user's message and respond ONLY with a JSON object containing:
                    {
                        "sentiment": "positive" | "neutral" | "negative",
                        "emotion": "satisfied" | "neutral" | "concerned" | "frustrated" | "angry",
                        "frustration_score": 0-100,
                        "key_concerns": ["list", "of", "concerns"],
                        "escalation_needed": true/false
                    }"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        sentiment_data = json.loads(response.choices[0].message.content)
        return sentiment_data
    except Exception as e:
        # Fallback sentiment analysis
        return {
            "sentiment": "neutral",
            "emotion": "neutral",
            "frustration_score": 0,
            "key_concerns": [],
            "escalation_needed": False
        }

def update_sentiment_tracking(sentiment_data):
    """Update sentiment history and track frustration levels"""
    st.session_state.sentiment_history.append({
        'timestamp': datetime.now().isoformat(),
        'sentiment': sentiment_data['sentiment'],
        'emotion': sentiment_data['emotion'],
        'frustration_score': sentiment_data['frustration_score']
    })
    
    st.session_state.current_sentiment = sentiment_data['sentiment']
    st.session_state.frustration_score = sentiment_data['frustration_score']
    
    # Escalation logic
    if sentiment_data['escalation_needed'] or sentiment_data['frustration_score'] > 70:
        st.session_state.escalation_triggered = True
        return True
    return False

# ================================
# AI CHATBOT CORE
# ================================

def generate_ai_response(user_message, context=None):
    """Generate AI response using GPT-4 with vehicle context"""
    
    # Build context from digital twin
    twin_context = st.session_state.digital_twin_data
    
    system_prompt = f"""You are VW NexaServe AI, an intelligent after-sales assistant for Volkswagen India. 
    
    CUSTOMER CONTEXT:
    - Vehicle: {twin_context['model']} ({twin_context['year']})
    - Vehicle ID: {twin_context['vehicle_id']}
    - Mileage: {twin_context['mileage']} km
    - Health Score: {twin_context['health_score']}/100
    - Last Service: {twin_context['last_service']}
    - Next Service Due: {twin_context['next_service_due']}
    
    YOUR CAPABILITIES:
    1. Diagnose vehicle issues using digital twin data
    2. Provide instant solutions for common problems
    3. Schedule service appointments
    4. Explain technical issues in simple language
    5. Offer AR remote assistance when needed
    6. Access blockchain-verified service history
    
    RESPONSE GUIDELINES:
    - Be empathetic and professional
    - Provide specific, actionable solutions
    - Reference the vehicle's actual data when relevant
    - Offer to escalate to human expert if issue is complex
    - Suggest AR guidance for visual problems
    - Always prioritize customer safety
    
    Respond conversationally and helpfully to the customer's query."""
    
    try:
        # Build message history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history (last 6 messages)
        for msg in st.session_state.messages[-6:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ I apologize, but I'm experiencing technical difficulties. Error: {str(e)}. Please try again or contact our support team."

# ================================
# ISSUE CLASSIFICATION
# ================================

def classify_issue(user_message):
    """Classify customer issue into categories"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Classify the automotive service issue into one of these categories.
                    Respond ONLY with a JSON object:
                    {
                        "category": "mechanical" | "electrical" | "maintenance" | "warranty" | "general_inquiry",
                        "severity": "low" | "medium" | "high" | "critical",
                        "requires_physical_inspection": true/false,
                        "suggested_action": "ai_resolution" | "ar_assistance" | "service_center" | "emergency",
                        "estimated_resolution_time": "minutes/hours/days"
                    }"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.2,
            max_tokens=150
        )
        
        classification = json.loads(response.choices[0].message.content)
        st.session_state.current_issue = classification
        return classification
        
    except Exception as e:
        return {
            "category": "general_inquiry",
            "severity": "low",
            "requires_physical_inspection": False,
            "suggested_action": "ai_resolution",
            "estimated_resolution_time": "minutes"
        }

# ================================
# BLOCKCHAIN SERVICE LEDGER
# ================================

def create_service_record(service_type, details, cost=0):
    """Create blockchain-verified service record"""
    
    record = {
        'record_id': str(uuid.uuid4()),
        'vehicle_id': st.session_state.digital_twin_data['vehicle_id'],
        'timestamp': datetime.now().isoformat(),
        'service_type': service_type,
        'details': details,
        'cost': cost,
        'technician': 'AI Assistant' if cost == 0 else 'Service Center',
        'status': 'completed',
        'blockchain_hash': hashlib.sha256(
            f"{datetime.now().isoformat()}{service_type}{details}".encode()
        ).hexdigest()[:16]
    }
    
    st.session_state.service_records.append(record)
    return record

def get_service_history():
    """Retrieve blockchain-verified service history"""
    return st.session_state.service_records

# ================================
# AR REMOTE ASSISTANCE SIMULATION
# ================================

def activate_ar_session():
    """Simulate AR remote assistance activation"""
    st.session_state.ar_session_active = True
    return {
        'session_id': str(uuid.uuid4()),
        'expert_assigned': 'VW Expert - Rajesh Kumar',
        'connection_quality': 'Excellent',
        'ar_features': [
            'Live Camera Feed',
            'Digital Annotations',
            'Component Highlighting',
            '3D Model Overlay',
            'Real-time Diagnostics'
        ]
    }

# ================================
# SMART APPOINTMENT BOOKING
# ================================

def schedule_appointment(preferred_date, service_type):
    """AI-powered appointment scheduling"""
    
    # Find optimal slot
    optimal_slot = {
        'date': preferred_date,
        'time': '10:00 AM',
        'service_center': 'VW Service Center - Whitefield, Bangalore',
        'estimated_duration': '2-3 hours',
        'assigned_technician': 'Senior Technician - Amit Sharma',
        'parts_availability': 'Confirmed',
        'booking_id': 'VW-APT-' + str(uuid.uuid4())[:8].upper(),
        'total_estimated_cost': '₹' + str(np.random.randint(3000, 15000))
    }
    
    st.session_state.appointment_scheduled = True
    
    # Create service record
    create_service_record(
        'Appointment Scheduled',
        f"{service_type} - {optimal_slot['date']} at {optimal_slot['time']}",
        0
    )
    
    return optimal_slot

# ================================
# DASHBOARD VISUALIZATIONS
# ================================

def render_digital_twin_dashboard():
    """Render comprehensive digital twin dashboard"""
    
    twin_data = st.session_state.digital_twin_data
    
    st.markdown('<div class="sub-header">🔧 Digital Twin - Real-time Vehicle Health</div>', unsafe_allow_html=True)
    
    # Overall Health Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Overall Health</h3>
            <h1>{twin_data['health_score']}%</h1>
            <p>Excellent Condition</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Current Mileage</h3>
            <h1>{twin_data['mileage']:,}</h1>
            <p>km driven</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        days_until_service = (datetime.strptime(twin_data['next_service_due'], '%Y-%m-%d') - datetime.now()).days
        st.markdown(f"""
        <div class="metric-card">
            <h3>Next Service</h3>
            <h1>{days_until_service}</h1>
            <p>days remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active Alerts</h3>
            <h1>{len(twin_data['predictive_alerts'])}</h1>
            <p>predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Component Health Visualization
    st.markdown("### Component Health Status")
    
    components = twin_data['components']
    component_names = ['Engine', 'Brakes', 'Transmission', 'Battery', 'Suspension']
    health_values = [
        components['engine']['health'],
        components['brakes']['health'],
        components['transmission']['health'],
        components['battery']['health'],
        components['suspension']['health']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=component_names,
        y=health_values,
        marker=dict(
            color=health_values,
            colorscale='RdYlGn',
            cmin=0,
            cmax=100,
            showscale=True
        ),
        text=[f"{v}%" for v in health_values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Component Health Analysis',
        yaxis_title='Health Score (%)',
        yaxis=dict(range=[0, 100]),
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tire Pressure Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Tire Health Status")
        tire_data = components['tires']
        
        fig_tire = go.Figure()
        
        fig_tire.add_trace(go.Scatterpolar(
            r=[tire_data['front_left'], tire_data['front_right'], 
               tire_data['rear_right'], tire_data['rear_left']],
            theta=['Front Left', 'Front Right', 'Rear Right', 'Rear Left'],
            fill='toself',
            name='Tire Health'
        ))
        
        fig_tire.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=350
        )
        
        st.plotly_chart(fig_tire, use_container_width=True)
    
    with col2:
        st.markdown("### Predictive Maintenance Alerts")
        
        twin_data = update_digital_twin_predictions(twin_data)
        
        if twin_data['predictive_alerts']:
            for alert in twin_data['predictive_alerts']:
                severity_color = {
                    'Low': '#10b981',
                    'Medium': '#f59e0b',
                    'High': '#ef4444',
                    'Critical': '#dc2626'
                }
                
                st.markdown(f"""
                <div class="service-card" style="border-left-color: {severity_color[alert['severity']]};">
                    <h4>⚠️ {alert['component']}</h4>
                    <p><strong>Severity:</strong> <span style="color: {severity_color[alert['severity']]};">{alert['severity']}</span></p>
                    <p>{alert['message']}</p>
                    <p><strong>Predicted Service Date:</strong> {alert['predicted_date']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No immediate maintenance required. All systems operating optimally!")

def render_sentiment_dashboard():
    """Render emotion intelligence dashboard"""
    
    if len(st.session_state.sentiment_history) > 0:
        st.markdown('<div class="sub-header">🧠 Emotional Intelligence Analytics</div>', unsafe_allow_html=True)
        
        # Sentiment timeline
        df_sentiment = pd.DataFrame(st.session_state.sentiment_history)
        df_sentiment['timestamp'] = pd.to_datetime(df_sentiment['timestamp'])
        
        fig = px.line(
            df_sentiment, 
            x='timestamp', 
            y='frustration_score',
            title='Customer Frustration Score Over Time',
            markers=True
        )
        
        fig.add_hline(
            y=70, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Escalation Threshold"
        )
        
        fig.update_layout(height=300, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
        
        # Current sentiment
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentiment_emoji = {
                'positive': '😊',
                'neutral': '😐',
                'negative': '😟'
            }
            st.metric(
                "Current Sentiment",
                sentiment_emoji.get(st.session_state.current_sentiment, '😐') + " " + st.session_state.current_sentiment.title()
            )
        
        with col2:
            st.metric(
                "Frustration Level",
                f"{st.session_state.frustration_score}/100",
                delta=None
            )
        
        with col3:
            if st.session_state.frustration_score > 70:
                st.error("🚨 Auto-escalation triggered!")
            else:
                st.success("✅ Sentiment stable")

def render_blockchain_ledger():
    """Render blockchain service history"""
    
    st.markdown('<div class="sub-header">⛓️ Blockchain-Verified Service History</div>', unsafe_allow_html=True)
    
    if st.session_state.service_records:
        for record in reversed(st.session_state.service_records):
            st.markdown(f"""
            <div class="service-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>📋 {record['service_type']}</h4>
                        <p><strong>Date:</strong> {datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M')}</p>
                        <p><strong>Details:</strong> {record['details']}</p>
                        <p><strong>Technician:</strong> {record['technician']}</p>
                        {f"<p><strong>Cost:</strong> ₹{record['cost']}</p>" if record['cost'] > 0 else ""}
                    </div>
                    <div>
                        <span class="blockchain-verified">🔒 Blockchain Verified</span>
                        <p style="font-size: 10px; margin-top: 5px;">Hash: {record['blockchain_hash']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 No service records yet. Your service history will appear here.")

# ================================
# MAIN APPLICATION
# ================================

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚗 VW NexaServe AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #667eea; margin-bottom: 30px;">"Where Every Customer Conversation Becomes a Service Revolution"</p>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.image("https://t4.ftcdn.net/jpg/03/67/41/07/360_F_367410748_MvYsCNThTfmCqGmvm5Zy856gseZUGHHT.jpg", width=200)
        
        st.markdown("---")
        
        page = st.radio(
            "🧭 Navigation",
            [
                "🏠 Home & Chat",
                "🔧 Digital Twin Dashboard",
                "📊 Sentiment Analytics",
                "⛓️ Service History",
                "📅 Book Appointment",
                "🎥 AR Remote Assistance",
                "ℹ️ About NexaServe AI"
            ]
        )
        
        st.markdown("---")
        
        # User Info
        if not st.session_state.user_authenticated:
            st.markdown("### 👤 Customer Login")
            user_name = st.text_input("Name", key="login_name")
            user_vehicle = st.text_input("Vehicle Reg. No.", key="login_vehicle")
            
            if st.button("🔐 Login", key="login_btn"):
                if user_name and user_vehicle:
                    st.session_state.user_authenticated = True
                    st.session_state.user_name = user_name
                    st.session_state.user_vehicle_id = user_vehicle
                    st.success(f"Welcome, {user_name}!")
                    st.rerun()
        else:
            st.success(f"✅ Logged in as: {st.session_state.user_name}")
            st.info(f"🚗 Vehicle: {st.session_state.user_vehicle_id}")
            
            if st.button("🚪 Logout"):
                st.session_state.user_authenticated = False
                st.session_state.user_name = ""
                st.rerun()
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 🔋 System Status")
        st.success("✅ AI Engine: Online")
        st.success("✅ Digital Twin: Active")
        st.success("✅ Blockchain: Synced")
        st.success("✅ AR Services: Ready")
    
    # Main Content Area
    if not st.session_state.user_authenticated:
        st.warning("👈 Please login from the sidebar to access VW NexaServe AI services")
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="service-card">
                <h3>🤖 AI-Powered Support</h3>
                <p>24/7 intelligent assistance with multilingual capabilities and instant problem resolution</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="service-card">
                <h3>🔮 Predictive Maintenance</h3>
                <p>Digital twin technology predicts issues before they occur, reducing emergency repairs by 60%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="service-card">
                <h3>⛓️ Blockchain Trust</h3>
                <p>Immutable service records with 100% transparency and fraud prevention</p>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    # Route to appropriate page
    if page == "🏠 Home & Chat":
        render_chat_interface()
    elif page == "🔧 Digital Twin Dashboard":
        render_digital_twin_dashboard()
    elif page == "📊 Sentiment Analytics":
        render_sentiment_dashboard()
    elif page == "⛓️ Service History":
        render_blockchain_ledger()
    elif page == "📅 Book Appointment":
        render_appointment_booking()
    elif page == "🎥 AR Remote Assistance":
        render_ar_interface()
    elif page == "ℹ️ About NexaServe AI":
        render_about_page()

def render_chat_interface():
    """Main conversational AI interface"""
    
    st.markdown('<div class="sub-header">💬 Intelligent Customer Service Chat</div>', unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Check Vehicle Health"):
            quick_message = "Can you show me my vehicle's current health status?"
            st.session_state.messages.append({"role": "user", "content": quick_message})
    
    with col2:
        if st.button("📅 Schedule Service"):
            quick_message = "I want to schedule a service appointment"
            st.session_state.messages.append({"role": "user", "content": quick_message})
    
    with col3:
        if st.button("🎥 Start AR Help"):
            st.session_state.ar_session_active = True
            quick_message = "I need visual guidance for my issue"
            st.session_state.messages.append({"role": "user", "content": quick_message})
    
    with col4:
        if st.button("🧾 View Service History"):
            quick_message = "Show me my service history"
            st.session_state.messages.append({"role": "user", "content": quick_message})
    
    st.markdown("---")
    
    # Chat Display Container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 NexaServe AI:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat Input
    st.markdown("---")
    
    # Multimodal Input Options
    input_mode = st.radio(
        "Input Mode:",
        ["💬 Text", "📷 Image Upload", "🎤 Voice (Simulated)"],
        horizontal=True
    )
    
    if input_mode == "💬 Text":
        user_input = st.chat_input("Type your message here... (e.g., 'My car is making a strange noise')")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Analyze sentiment
            sentiment_data = analyze_sentiment(user_input)
            update_sentiment_tracking(sentiment_data)
            
            # Classify issue
            issue_classification = classify_issue(user_input)
            
            # Generate AI response
            with st.spinner("🤖 NexaServe AI is thinking..."):
                ai_response = generate_ai_response(user_input)
                
                # Add contextual information based on classification
                if issue_classification['suggested_action'] == 'ar_assistance':
                    ai_response += "\n\n🎥 **Recommendation:** This issue would benefit from AR visual guidance. Would you like to start an AR session with our expert?"
                elif issue_classification['suggested_action'] == 'service_center':
                    ai_response += "\n\n🔧 **Recommendation:** This requires physical inspection. I can help you schedule an appointment at the nearest service center."
                elif issue_classification['severity'] == 'critical':
                    ai_response += "\n\n🚨 **URGENT:** This appears to be a safety-critical issue. I'm escalating this to our emergency support team immediately."
                
                # Check for escalation
                if sentiment_data.get('escalation_needed'):
                    ai_response += "\n\n👨‍💼 **Auto-Escalation:** I've detected your frustration. Connecting you with a senior service advisor now..."
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            st.rerun()
    
    elif input_mode == "📷 Image Upload":
        st.markdown("### Upload Vehicle Issue Image")
        uploaded_image = st.file_uploader(
            "Take a photo of the problem area",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of the issue for visual diagnosis"
        )
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                if st.button("🔍 Analyze Image with AI"):
                    with st.spinner("Analyzing image with computer vision..."):
                        time.sleep(2)  # Simulate processing
                        
                        # Simulated image analysis
                        analysis_result = """
                        **Visual Diagnosis Complete:**
                        
                        ✅ **Detected Component:** Front brake disc
                        ⚠️ **Issue Identified:** Excessive wear on brake pads (approx. 65%)
                        🔴 **Severity:** Medium-High
                        
                        **Recommended Action:**
                        1. Schedule brake pad replacement within 2 weeks
                        2. Estimated cost: ₹8,500 - ₹12,000
                        3. Service duration: 2-3 hours
                        
                        Would you like me to schedule an appointment?
                        """
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": analysis_result
                        })
                        
                        st.success("Image analysis complete!")
                        st.rerun()
    
    elif input_mode == "🎤 Voice (Simulated)":
        st.markdown("### Voice Input (Simulation)")
        st.info("🎤 In production, this would activate real-time voice input using Whisper API")
        
        sample_voice_inputs = [
            "My car's engine is making a clicking sound",
            "The check engine light came on this morning",
            "I need to schedule my regular service",
            "There's a burning smell from the brakes"
        ]
        
        selected_voice = st.selectbox("Simulate voice input:", sample_voice_inputs)
        
        if st.button("🎙️ Send Voice Message"):
            st.session_state.messages.append({"role": "user", "content": f"🎤 (Voice): {selected_voice}"})
            
            with st.spinner("Processing voice input..."):
                time.sleep(1)
                ai_response = generate_ai_response(selected_voice)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            st.rerun()

def render_appointment_booking():
    """Smart appointment booking interface"""
    
    st.markdown('<div class="sub-header">📅 AI-Powered Appointment Scheduling</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Schedule Your Service")
        
        service_type = st.selectbox(
            "Service Type",
            [
                "Regular Maintenance",
                "Engine Diagnostics",
                "Brake Service",
                "Oil Change",
                "Tire Replacement",
                "Battery Replacement",
                "AC Service",
                "Transmission Service",
                "Other"
            ]
        )
        
        preferred_date = st.date_input(
            "Preferred Date",
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=60)
        )
        
        location = st.selectbox(
            "Service Center Location",
            [
                "VW Service Center - Whitefield, Bangalore",
                "VW Service Center - Koramangala, Bangalore",
                "VW Service Center - Hebbal, Bangalore",
                "VW Service Center - Electronic City, Bangalore"
            ]
        )
        
        issue_description = st.text_area(
            "Describe the issue or service needed",
            placeholder="E.g., Strange noise from engine, regular 10,000 km service, brake pads replacement..."
        )
        
        if st.button("🔍 Find Optimal Slot", type="primary"):
            with st.spinner("AI is finding the best slot for you..."):
                time.sleep(2)
                
                appointment = schedule_appointment(preferred_date.strftime('%Y-%m-%d'), service_type)
                
                st.success("✅ Optimal slot found!")
                
                st.markdown(f"""
                <div class="service-card">
                    <h3>📋 Appointment Confirmation</h3>
                    <p><strong>Booking ID:</strong> {appointment['booking_id']}</p>
                    <p><strong>Date & Time:</strong> {appointment['date']} at {appointment['time']}</p>
                    <p><strong>Location:</strong> {appointment['service_center']}</p>
                    <p><strong>Service Type:</strong> {service_type}</p>
                    <p><strong>Assigned Technician:</strong> {appointment['assigned_technician']}</p>
                    <p><strong>Estimated Duration:</strong> {appointment['estimated_duration']}</p>
                    <p><strong>Parts Status:</strong> ✅ {appointment['parts_availability']}</p>
                    <p><strong>Estimated Cost:</strong> {appointment['total_estimated_cost']}</p>
                    <span class="blockchain-verified">⛓️ Recorded on Blockchain</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🗓️ Available Slots")
        
        # Generate sample available slots
        slots = []
        for i in range(5):
            slot_date = datetime.now() + timedelta(days=i)
            slots.append({
                'date': slot_date.strftime('%Y-%m-%d'),
                'morning': np.random.choice(['Available', 'Busy', 'Available']),
                'afternoon': np.random.choice(['Available', 'Busy', 'Available']),
                'evening': np.random.choice(['Available', 'Busy', 'Limited'])
            })
        
        df_slots = pd.DataFrame(slots)
        st.dataframe(df_slots, use_container_width=True)

def render_ar_interface():
    """AR Remote Assistance Interface"""

    st.markdown('<div class="sub-header">🎥 AR Remote Assistance</div>', unsafe_allow_html=True)

    if not st.session_state.ar_session_active:
        st.markdown("""
        <div class="service-card">
            <h3>🎯 See-What-I-See AR Support</h3>
            <p>Connect with our expert technicians through augmented reality for real-time visual guidance.</p>
            <h4>Features:</h4>
            <ul>
                <li>✅ Live camera feed sharing</li>
                <li>✅ Real-time expert annotations</li>
                <li>✅ 3D component overlays</li>
                <li>✅ Step-by-step AR instructions</li>
                <li>✅ AI + Expert hybrid diagnostics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start AR Session", type="primary"):
            ar_session = activate_ar_session()
            st.session_state.ar_session_data = ar_session
            st.session_state.ar_session_active = True
            st.success("AR Session activated!")
            st.rerun()
    else:
        ar_data = st.session_state.ar_session_data
        if ar_data:
            st.markdown(f"""
            <div class="ar-active">
                <h3>🔴 LIVE AR SESSION</h3>
                <p><strong>Session ID:</strong> {ar_data['session_id']}</p>
                <p><strong>Expert:</strong> {ar_data['expert_assigned']}</p>
                <p><strong>Connection:</strong> {ar_data['connection_quality']}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("### 📹 Live Camera Feed (Simulated)")
                st.info("📱 In production, this displays your device's camera feed with AR overlays")
                st.image("https://www.shutterstock.com/image-photo/explore-complexities-modern-engine-compartments-260nw-2669845105.jpg",
                         caption="AR View: Engine Bay with Component Highlighting",
                         use_container_width=True)

                st.markdown("""
                <div class="service-card">
                    <h4>🎯 AR Annotations Active:</h4>
                    <ul>
                        <li>🔴 Battery terminals highlighted</li>
                        <li>🟢 Oil dipstick location marked</li>
                        <li>🟡 Air filter compartment outlined</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("### 🛠️ AR Tools")
                for feature in ar_data['ar_features']:
                    st.success(f"✅ {feature}")

                st.markdown("---")
                st.markdown("### 💬 Expert Chat")
                expert_messages = [
                    "Expert: I can see the battery terminals. Let's check the connections.",
                    "You: Should I disconnect it?",
                    "Expert: Not yet. First, check if the terminals are corroded."
                ]
                for msg in expert_messages:
                    st.text(msg)
                st.text_input("Message expert:", key="ar_chat")

            if st.button("🛑 End AR Session"):
                st.session_state.ar_session_active = False
                st.session_state.ar_session_data = None
                create_service_record(
                    'AR Remote Assistance',
                    f"Session with {ar_data['expert_assigned']} - Issue diagnosed remotely",
                    0
                )
                st.success("AR session ended. Diagnostic report saved to your service history.")
                st.rerun()
        else:
            st.info("AR session data is not initialized. Please start a new AR session to proceed.")


def render_about_page():
    """About VW NexaServe AI"""
    
    st.markdown('<div class="sub-header">ℹ️ About VW NexaServe AI</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🚗 VW NexaServe AI - Multimodal Intelligent After-Sales Ecosystem
    
    **"Where Every Customer Conversation Becomes a Service Revolution"**
    
    ### 🎯 Solution Overview
    
    VW NexaServe AI is a groundbreaking multimodal, intelligent after-sales ecosystem designed to revolutionize 
    automotive customer service by transforming reactive support into a proactive, smart, and emotionally aware experience.
    
    ### 🏆 Key Innovations
    
    #### 1️⃣ Multimodal AI Intelligence
    - **Text + Voice + Visual + AR** in one integrated platform
    - Seamless interaction across multiple channels
    - Natural language understanding in multiple languages
    
    #### 2️⃣ Emotional Intelligence Layer
    - Real-time sentiment analysis detecting frustration/satisfaction
    - Automatic escalation when customer frustration exceeds threshold
    - Tone-aware responses adapting to customer emotions
    
    #### 3️⃣ Digital Twin Technology
    - Real-time virtual replica of every vehicle
    - Predictive maintenance alerts before failures occur
    - ML-powered health monitoring of all systems
    
    #### 4️⃣ Blockchain Service Ledger
    - Immutable service records eliminating fraud
    - 100% transparent service history
    - Smart contract automation for warranty claims
    
    #### 5️⃣ AR Remote Assistance
    - See-what-I-see expert support
    - Real-time AR annotations and guidance
    - 60% reduction in service center visits
    
    #### 6️⃣ Edge + Cloud Hybrid
    - Works offline with on-device AI
    - Sub-200ms response times
    - Auto-sync when connectivity restored
    
    #### 7️⃣ Privacy-First Architecture
    - Federated learning keeps data on-device
    - No sensitive data collection
    - GDPR compliant design
    
    ### 📊 Impact Metrics
    
    - **85%+** First-contact resolution rate
    - **60%** Reduction in service visits via remote AR diagnosis
    - **80%** Faster warranty claim processing
    - **90%** Prevention of negative reviews through emotion detection
    - **24/7** Availability with multilingual support
    
    ### 🛠️ Technology Stack
    
    **Frontend:** Streamlit, React Native (Mobile)  
    **AI/ML:** OpenAI GPT-4, Gemini Pro, Hume AI (Emotion)  
    **Backend:** Node.js, Python FastAPI, GraphQL  
    **Blockchain:** Hyperledger Fabric, Smart Contracts  
    **Edge Computing:** TensorFlow Lite, ONNX Runtime  
    **AR Platform:** ARCore/ARKit, Unity AR Foundation  
    **Cloud:** Multi-cloud (AWS/Azure/GCP)  
    
    ### 👥 Team & Hackathon
    
    **Event:** i.mobilothon 5.0 by Volkswagen  
    **Problem Statement:** Transforming After-Sales Support  
    **Solution:** VW NexaServe AI  
    
    ### 📞 Support
    
    For technical support or inquiries about NexaServe AI:
    - Email: support@vw-nexaserve.ai
    - Phone: 1800-123-VWAI (1800-123-8924)
    - WhatsApp: Available through integrated chat
    
    ---
    
    **Built with ❤️ for Volkswagen's Future of Mobility**
    """)
    
    # Technology Architecture Diagram
    st.markdown("### 🏗️ System Architecture")
    
    architecture_layers = {
        'Layer': [
            'Layer 1: User Interface',
            'Layer 2: API Gateway & Edge',
            'Layer 3: Multimodal AI Engine',
            'Layer 4: Core Services',
            'Layer 5: Blockchain Layer',
            'Layer 6: Data & ML',
            'Layer 7: Integration',
            'Layer 8: Infrastructure'
        ],
        'Components': [
            'Mobile Apps, Web, WhatsApp, Voice, AR Glasses',
            'Load Balancing, Authentication, Edge AI Processing',
            'GPT-4, Gemini Pro, Computer Vision, Emotion AI',
            'Service Orchestration, Digital Twin, AR Support, Automation',
            'Hyperledger Fabric, Smart Contracts, Service Records',
            'Federated Learning, Predictive Models, Vector DB',
            'VW Service Systems, Inventory, CRM, Telematics',
            'Multi-cloud, Edge Nodes, Monitoring'
        ]
    }
    
    df_arch = pd.DataFrame(architecture_layers)
    st.dataframe(df_arch, use_container_width=True, hide_index=True)

# ================================
# RUN APPLICATION
# ================================

if __name__ == "__main__":
    main()
