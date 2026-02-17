import streamlit as st
import pandas as pd
import pickle
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI-ReHaB Stress Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px;
        padding: 50px 40px;
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(78, 205, 196, 0.08) 0%, transparent 50%);
        animation: pulse-bg 6s ease-in-out infinite;
    }
    @keyframes pulse-bg {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        position: relative;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #a8a8b3;
        position: relative;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Metric info cards */
    .metric-info-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 30px 25px;
        border: 1px solid rgba(78, 205, 196, 0.15);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .metric-info-card:hover {
        border-color: rgba(78, 205, 196, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(78, 205, 196, 0.1);
    }
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        display: block;
    }
    .metric-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #4ECDC4;
        margin-bottom: 8px;
    }
    .metric-unit {
        font-size: 0.85rem;
        color: #6c6c80;
        margin-bottom: 12px;
        font-weight: 500;
    }
    .metric-description {
        font-size: 0.95rem;
        color: #c4c4cc;
        line-height: 1.7;
    }
    .metric-why {
        margin-top: 14px;
        padding-top: 14px;
        border-top: 1px solid rgba(78, 205, 196, 0.1);
        font-size: 0.88rem;
        color: #8d8d99;
        line-height: 1.6;
    }
    .metric-why strong {
        color: #FF6B6B;
    }

    /* Section headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #e1e1e6;
        margin: 40px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(78, 205, 196, 0.2);
    }

    /* Graph explanation cards */
    .graph-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 28px;
        border-left: 4px solid;
        margin-bottom: 20px;
    }
    .graph-card-green { border-left-color: #00CC96; }
    .graph-card-coral { border-left-color: #FF6B6B; }
    .graph-card-teal { border-left-color: #4ECDC4; }
    .graph-card-orange { border-left-color: #FFA500; }
    .graph-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #e1e1e6;
        margin-bottom: 8px;
    }
    .graph-desc {
        font-size: 0.92rem;
        color: #a8a8b3;
        line-height: 1.65;
    }

    /* Condition legend pills */
    .condition-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }
    .pill-green { background: rgba(0, 204, 150, 0.15); color: #00CC96; border: 1px solid rgba(0, 204, 150, 0.3); }
    .pill-orange { background: rgba(255, 165, 0, 0.15); color: #FFA500; border: 1px solid rgba(255, 165, 0, 0.3); }
    .pill-red { background: rgba(239, 85, 59, 0.15); color: #EF553B; border: 1px solid rgba(239, 85, 59, 0.3); }

    /* How it works steps */
    .step-container {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 18px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .step-number {
        background: linear-gradient(135deg, #4ECDC4, #44a08d);
        color: #fff;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.95rem;
        flex-shrink: 0;
    }
    .step-text {
        color: #c4c4cc;
        font-size: 0.95rem;
        line-height: 1.6;
        padding-top: 6px;
    }
    .step-text strong {
        color: #e1e1e6;
    }

    /* General styling */
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stAlert {
        margin-top: 10px;
    }

    /* Footer */
    .footer-styled {
        text-align: center;
        color: #6c6c80;
        padding: 30px 20px;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. LOAD RESOURCES
# ==========================================
@st.cache_resource
def load_resources():
    """Load ML model and sample data"""
    try:
        with open('stress_model.pkl', 'rb') as f:
            model = pickle.load(f)
        # Load sample data (simulating a 5-minute session at 1 Hz)
        df = pd.read_csv('train.csv').sample(300, random_state=42).reset_index(drop=True)
        return model, df
    except FileNotFoundError as e:
        st.error(f"❌ Required file not found: {e.filename}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading resources: {str(e)}")
        st.stop()


model, df_stream = load_resources()


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def prepare_features(row):
    """Prepare model input from raw physiological data with error handling"""
    try:
        hr = row.get('HR', 60000 / max(row['MEAN_RR'], 1))  # Avoid division by zero
        return pd.DataFrame({
            'MEAN_RR': [row['MEAN_RR']],
            'RMSSD': [row['RMSSD']],
            'LF_HF': [row['LF_HF']],
            'HR': [hr]
        })
    except Exception as e:
        st.error(f"Feature preparation error: {str(e)}")
        return None


def get_status_color(condition):
    """Return color and emoji for condition"""
    color_map = {
        "no stress": ("green", "🟢"),
        "interruption": ("orange", "🟡"),
        "time pressure": ("red", "🔴")
    }
    return color_map.get(condition.lower(), ("gray", "⚪"))


def calculate_session_stats(history_df):
    """Calculate comprehensive session statistics"""
    if history_df.empty:
        return None

    stats = {
        'duration': (history_df['Time'].max() - history_df['Time'].min()).total_seconds(),
        'avg_hr': history_df['Heart Rate'].mean(),
        'max_hr': history_df['Heart Rate'].max(),
        'min_hr': history_df['Heart Rate'].min(),
        'avg_hrv': history_df['HRV (RMSSD)'].mean(),
        'stress_percentage': (history_df['Condition'] != 'no stress').sum() / len(history_df) * 100
    }
    return stats


# ==========================================
# 4. SESSION STATE INITIALIZATION
# ==========================================
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False

if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

if 'session_start_time' not in st.session_state:
    st.session_state['session_start_time'] = None

# ==========================================
# 5. TABS LAYOUT
# ==========================================
tab_intro, tab1, tab2 = st.tabs(["🏠 Introduction", "🔴 Live Monitor", "📊 Session Report"])

# ==========================================
# TAB INTRO: INTRODUCTION & METRIC GUIDE
# ==========================================
with tab_intro:
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">AI-ReHaB Stress Analytics</div>
        <div class="hero-subtitle">
            Real-time physiological monitoring powered by machine learning.
            Detect stress patterns through heart rate variability analysis to support
            rehabilitation outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- KEY METRICS SECTION ----------
    st.markdown('<div class="section-header">Key Physiological Metrics</div>', unsafe_allow_html=True)
    st.markdown(
        "These are the four biomarkers our model uses to classify stress states in real time.",
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4, gap="medium")

    with m1:
        st.markdown("""
        <div class="metric-info-card">
            <span class="metric-icon">💓</span>
            <div class="metric-name">Heart Rate (HR)</div>
            <div class="metric-unit">Measured in BPM (beats per minute)</div>
            <div class="metric-description">
                The number of times your heart beats each minute.
                It reflects overall cardiovascular demand and is one of the most
                direct indicators of physical and psychological arousal.
            </div>
            <div class="metric-why">
                <strong>Why it matters:</strong> HR rises under stress as the sympathetic
                nervous system activates the fight-or-flight response. Sustained elevation
                can indicate chronic stress exposure.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-info-card">
            <span class="metric-icon">📊</span>
            <div class="metric-name">MEAN RR Interval</div>
            <div class="metric-unit">Measured in milliseconds (ms)</div>
            <div class="metric-description">
                The average time between consecutive heartbeats (R-peaks in an ECG).
                A longer interval means a slower heart rate; a shorter interval
                means a faster heart rate.
            </div>
            <div class="metric-why">
                <strong>Why it matters:</strong> MEAN_RR captures the baseline cardiac rhythm.
                Drops in MEAN_RR during a session signal increased cardiac demand,
                often linked to cognitive load or emotional stress.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-info-card">
            <span class="metric-icon">🔬</span>
            <div class="metric-name">RMSSD (HRV)</div>
            <div class="metric-unit">Measured in milliseconds (ms)</div>
            <div class="metric-description">
                Root Mean Square of Successive Differences between heartbeats.
                This is the gold-standard short-term measure of Heart Rate Variability (HRV),
                reflecting parasympathetic (vagal) activity.
            </div>
            <div class="metric-why">
                <strong>Why it matters:</strong> High RMSSD = strong vagal tone = relaxation.
                Low RMSSD = reduced vagal control = stress. A drop of 20%+ from baseline
                is clinically significant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown("""
        <div class="metric-info-card">
            <span class="metric-icon">⚖️</span>
            <div class="metric-name">LF/HF Ratio</div>
            <div class="metric-unit">Unitless ratio</div>
            <div class="metric-description">
                The ratio of Low Frequency to High Frequency power in the HRV spectrum.
                LF captures sympathetic + parasympathetic activity, while HF reflects
                parasympathetic (vagal) control.
            </div>
            <div class="metric-why">
                <strong>Why it matters:</strong> A rising LF/HF ratio indicates a shift
                toward sympathetic dominance — your body's stress response taking over.
                Values above 2.0 often indicate significant stress.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- STRESS CONDITIONS SECTION ----------
    st.markdown('<div class="section-header">Stress Conditions Detected</div>', unsafe_allow_html=True)
    st.markdown(
        "Our Random Forest classifier (88% accuracy) categorizes each moment into one of three states:",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="graph-card graph-card-green">
            <div class="graph-title">🟢 No Stress</div>
            <div class="graph-desc">
                The participant shows a relaxed physiological profile: stable heart rate near
                baseline, high HRV (strong vagal tone), and a balanced LF/HF ratio.
                This is the target state during rehabilitation exercises.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="graph-card graph-card-orange">
            <div class="graph-title">🟡 Interruption</div>
            <div class="graph-desc">
                An external disruption triggers an acute orienting response: brief HR spike,
                temporary HRV dip, and transient LF/HF increase.
                These episodes indicate task-switching cognitive cost.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="graph-card graph-card-coral">
            <div class="graph-title">🔴 Time Pressure</div>
            <div class="graph-desc">
                Sustained sympathetic activation from deadline-driven demands: elevated HR,
                suppressed HRV, and a high LF/HF ratio.
                Prolonged exposure can impair recovery and rehabilitation progress.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- GRAPHS EXPLAINED SECTION ----------
    st.markdown('<div class="section-header">Understanding the Graphs</div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2, gap="medium")

    with g1:
        st.markdown("""
        <div class="graph-card graph-card-coral">
            <div class="graph-title">Live Dual-Axis Chart (Monitor Tab)</div>
            <div class="graph-desc">
                Shows real-time Heart Rate (red line, left axis) and HRV/RMSSD
                (teal line, right axis) over a rolling 60-second window. A dashed gray
                line marks the 70 BPM baseline. When the red line rises while the
                teal line drops, the participant is entering a stress state.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="graph-card graph-card-green">
            <div class="graph-title">Condition Distribution Pie Chart</div>
            <div class="graph-desc">
                A donut chart breaking down what percentage of the session was spent
                in each condition. A healthy session should show a large green
                (no stress) slice. High orange or red proportions indicate
                the session was cognitively demanding.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown("""
        <div class="graph-card graph-card-teal">
            <div class="graph-title">Heart Rate Timeline Scatter Plot</div>
            <div class="graph-desc">
                Each data point represents a single second's heart rate reading,
                color-coded by the model's stress classification. Clusters of red
                or orange dots reveal when stress episodes occurred and how long
                they lasted, helping clinicians identify patterns.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="graph-card graph-card-orange">
            <div class="graph-title">Average HR by Condition Bar Chart</div>
            <div class="graph-desc">
                Compares the mean heart rate across the three conditions. A large
                gap between "no stress" and "time pressure" bars confirms strong
                physiological differentiation and validates the model's clinical
                relevance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- HOW IT WORKS SECTION ----------
    st.markdown('<div class="section-header">How to Use This Platform</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(145deg, #1a1a2e, #16213e); border-radius: 16px; padding: 30px; border: 1px solid rgba(78,205,196,0.1);">
        <div class="step-container">
            <div class="step-number">1</div>
            <div class="step-text"><strong>Navigate to the Live Monitor tab</strong> — this is where real-time streaming happens.</div>
        </div>
        <div class="step-container">
            <div class="step-number">2</div>
            <div class="step-text"><strong>Click Start Session</strong> — the system begins processing 300 physiological samples (simulating a 5-minute session at 1 Hz).</div>
        </div>
        <div class="step-container">
            <div class="step-number">3</div>
            <div class="step-text"><strong>Watch the live chart and metrics update</strong> — HR, HRV, and the model's stress classification refresh each second.</div>
        </div>
        <div class="step-container">
            <div class="step-number">4</div>
            <div class="step-text"><strong>Stop or let the session complete</strong> — you can pause at any time or let all 300 samples process.</div>
        </div>
        <div class="step-container" style="border-bottom: none;">
            <div class="step-number">5</div>
            <div class="step-text"><strong>Review the Session Report tab</strong> — get clinical insights, condition breakdowns, physiological impact analysis, and export your data as CSV.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- MODEL INFO CALLOUT ----------
    st.markdown('<div class="section-header">About the Model</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(145deg, #1a1a2e, #16213e); border-radius: 16px; padding: 30px; border: 1px solid rgba(78,205,196,0.1);">
        <div class="graph-desc" style="margin-bottom: 12px;">
            The stress classifier is a <strong style="color: #4ECDC4;">Random Forest</strong> model
            trained on <strong style="color: #4ECDC4;">369,289 HRV samples</strong> from the SWELL dataset.
            It uses four input features (HR, MEAN_RR, RMSSD, LF/HF) to classify physiological
            state into three categories with <strong style="color: #4ECDC4;">88% accuracy</strong>.
        </div>
        <div style="display: flex; gap: 30px; flex-wrap: wrap; margin-top: 16px;">
            <div>
                <span style="color: #6c6c80; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Algorithm</span><br>
                <span style="color: #e1e1e6; font-weight: 600;">Random Forest (100 trees)</span>
            </div>
            <div>
                <span style="color: #6c6c80; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Features</span><br>
                <span style="color: #e1e1e6; font-weight: 600;">HR, MEAN_RR, RMSSD, LF/HF</span>
            </div>
            <div>
                <span style="color: #6c6c80; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Accuracy</span><br>
                <span style="color: #e1e1e6; font-weight: 600;">88.03%</span>
            </div>
            <div>
                <span style="color: #6c6c80; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Training Samples</span><br>
                <span style="color: #e1e1e6; font-weight: 600;">369,289</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# TAB 1: LIVE MONITORING
# ==========================================
with tab1:
    st.title("🫀 Real-Time Physiological Monitoring")
    st.markdown("---")

    # Control buttons
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 3])

    with col_btn1:
        if st.button("▶️ Start Session", disabled=st.session_state['is_running'], use_container_width=True):
            st.session_state['is_running'] = True
            st.session_state['current_index'] = 0
            st.session_state['history'] = []
            st.session_state['session_start_time'] = datetime.now()
            st.rerun()

    with col_btn2:
        if st.button("⏸️ Stop Session", disabled=not st.session_state['is_running'], use_container_width=True):
            st.session_state['is_running'] = False
            st.rerun()

    with col_btn3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state['is_running'] = False
            st.session_state['current_index'] = 0
            st.session_state['history'] = []
            st.session_state['session_start_time'] = None
            st.rerun()

    # Metrics Display
    col1, col2, col3, col4 = st.columns(4)
    metric_hr = col1.empty()
    metric_hrv = col2.empty()
    metric_status = col3.empty()
    metric_time = col4.empty()

    # Charts
    st.markdown("### Physiological Signals")
    chart_placeholder = st.empty()

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Live streaming loop
    if st.session_state['is_running'] and st.session_state['current_index'] < len(df_stream):
        i = st.session_state['current_index']
        row = df_stream.iloc[i]

        # Prepare features
        input_data = prepare_features(row)

        if input_data is not None:
            # Predict
            try:
                pred = model.predict(input_data)[0]
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                st.session_state['is_running'] = False
                st.stop()

            # Calculate elapsed time
            elapsed = timedelta(seconds=i)
            timestamp = st.session_state['session_start_time'] + elapsed

            # Save to history
            st.session_state['history'].append({
                'Time': timestamp,
                'Heart Rate': input_data['HR'].iloc[0],
                'HRV (RMSSD)': row['RMSSD'],
                'LF/HF': row['LF_HF'],
                'Condition': pred
            })

            # Update metrics
            color, emoji = get_status_color(pred)

            metric_hr.metric(
                "Heart Rate",
                f"{int(input_data['HR'].iloc[0])} BPM",
                delta=f"{int(input_data['HR'].iloc[0]) - 70} from baseline"
            )
            metric_hrv.metric(
                "HRV (RMSSD)",
                f"{row['RMSSD']:.1f} ms"
            )
            metric_status.markdown(f"### {emoji} {pred.upper()}")
            metric_time.metric(
                "Session Time",
                f"{int(elapsed.total_seconds())}s"
            )

            # Update live chart (last 60 seconds)
            history_df = pd.DataFrame(st.session_state['history'][-60:])

            if not history_df.empty:
                fig = go.Figure()

                # Heart Rate trace
                fig.add_trace(go.Scatter(
                    x=history_df['Time'],
                    y=history_df['Heart Rate'],
                    name='Heart Rate',
                    line=dict(color='#FF6B6B', width=2),
                    mode='lines'
                ))

                # HRV trace on secondary axis
                fig.add_trace(go.Scatter(
                    x=history_df['Time'],
                    y=history_df['HRV (RMSSD)'],
                    name='HRV (RMSSD)',
                    line=dict(color='#4ECDC4', width=2),
                    mode='lines',
                    yaxis='y2'
                ))

                # Add baseline reference lines
                fig.add_hline(y=70, line_dash="dash", line_color="gray",
                              annotation_text="Baseline HR", opacity=0.5)

                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(title="Time"),
                    yaxis=dict(title="Heart Rate (BPM)", side='left'),
                    yaxis2=dict(title="HRV (ms)", overlaying='y', side='right'),
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )

                chart_placeholder.plotly_chart(fig, use_container_width=True)

            # Update progress
            progress = (i + 1) / len(df_stream)
            progress_bar.progress(progress)
            status_text.text(f"Processing sample {i + 1} of {len(df_stream)}")

            # Increment index and continue
            st.session_state['current_index'] += 1
            time.sleep(0.1)  # Faster refresh for better UX
            st.rerun()

    elif st.session_state['is_running']:
        # Session completed
        st.session_state['is_running'] = False
        st.success("✅ Session completed! Switch to the 'Session Report' tab for detailed analysis.")
        st.balloons()

# ==========================================
# TAB 2: SESSION REPORT
# ==========================================
with tab2:
    st.title("📊 Clinical Session Report")
    st.markdown("---")

    if len(st.session_state['history']) > 0:
        report_df = pd.DataFrame(st.session_state['history'])
        stats = calculate_session_stats(report_df)

        # Session Overview
        st.subheader("📋 Session Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Duration", f"{int(stats['duration'])}s")
        with col2:
            st.metric("Avg Heart Rate", f"{stats['avg_hr']:.0f} BPM")
        with col3:
            st.metric("Avg HRV", f"{stats['avg_hrv']:.1f} ms")
        with col4:
            st.metric("Stress Load", f"{stats['stress_percentage']:.1f}%")

        st.markdown("---")

        # Two-column layout for visualizations
        viz_col1, viz_col2 = st.columns([1, 1])

        # 1. Stress Distribution (Pie Chart)
        with viz_col1:
            st.subheader("Condition Distribution")
            stress_counts = report_df['Condition'].value_counts()
            fig_pie = px.pie(
                values=stress_counts.values,
                names=stress_counts.index,
                title="",
                color_discrete_map={
                    "no stress": "#00CC96",
                    "interruption": "#FFA500",
                    "time pressure": "#EF553B"
                },
                hole=0.3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

        # 2. Heart Rate Timeline with Condition Overlay
        with viz_col2:
            st.subheader("Heart Rate Timeline")
            fig_timeline = px.scatter(
                report_df,
                x='Time',
                y='Heart Rate',
                color='Condition',
                color_discrete_map={
                    "no stress": "#00CC96",
                    "interruption": "#FFA500",
                    "time pressure": "#EF553B"
                },
                title=""
            )
            fig_timeline.update_traces(marker=dict(size=8))
            fig_timeline.update_layout(height=350, xaxis_title="Time", yaxis_title="Heart Rate (BPM)")
            st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("---")

        # 3. Physiological Impact Analysis
        st.subheader("🧠 Physiological Impact by Condition")

        analysis_col1, analysis_col2 = st.columns([2, 1])

        with analysis_col1:
            # Group by condition
            summary = report_df.groupby('Condition').agg({
                'Heart Rate': ['mean', 'std', 'min', 'max'],
                'HRV (RMSSD)': ['mean', 'std'],
                'LF/HF': 'mean'
            }).round(2)

            summary.columns = ['HR Mean', 'HR Std', 'HR Min', 'HR Max', 'HRV Mean', 'HRV Std', 'LF/HF Ratio']
            st.dataframe(summary, use_container_width=True)

        with analysis_col2:
            # Bar chart comparison
            fig_bar = px.bar(
                summary.reset_index(),
                x='Condition',
                y='HR Mean',
                title="Average Heart Rate by Condition",
                color='Condition',
                color_discrete_map={
                    "no stress": "#00CC96",
                    "interruption": "#FFA500",
                    "time pressure": "#EF553B"
                }
            )
            fig_bar.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_bar, use_container_width=True)

        # 4. Clinical Insights
        st.markdown("---")
        st.subheader("💡 Clinical Insights")

        # Calculate insights
        if 'no stress' in summary.index:
            baseline_hrv = summary.loc['no stress', 'HRV Mean']
            baseline_hr = summary.loc['no stress', 'HR Mean']

            insights = []

            # Time pressure analysis
            if 'time pressure' in summary.index:
                stress_hrv = summary.loc['time pressure', 'HRV Mean']
                stress_hr = summary.loc['time pressure', 'HR Mean']

                hrv_drop = ((baseline_hrv - stress_hrv) / baseline_hrv) * 100
                hr_increase = ((stress_hr - baseline_hr) / baseline_hr) * 100

                insights.append({
                    'type': 'warning' if hrv_drop > 20 else 'info',
                    'message': f"**Time Pressure Response:** HRV decreased by {hrv_drop:.1f}% and heart rate increased by {hr_increase:.1f}% compared to baseline, indicating {'significant' if hrv_drop > 20 else 'moderate'} sympathetic nervous system activation."
                })

            # Interruption analysis
            if 'interruption' in summary.index:
                int_hrv = summary.loc['interruption', 'HRV Mean']
                int_drop = ((baseline_hrv - int_hrv) / baseline_hrv) * 100

                insights.append({
                    'type': 'info',
                    'message': f"**Interruption Response:** HRV decreased by {int_drop:.1f}% during interruptions, suggesting acute stress response to task switching."
                })

            # Overall assessment
            if stats['stress_percentage'] > 50:
                insights.append({
                    'type': 'warning',
                    'message': f"⚠️ **High Stress Load:** Patient spent {stats['stress_percentage']:.1f}% of the session under stress conditions. Consider stress management interventions."
                })
            else:
                insights.append({
                    'type': 'success',
                    'message': f"✅ **Manageable Stress Load:** Patient maintained good resilience with only {stats['stress_percentage']:.1f}% of session under stress."
                })

            # Display insights
            for insight in insights:
                if insight['type'] == 'warning':
                    st.warning(insight['message'])
                elif insight['type'] == 'success':
                    st.success(insight['message'])
                else:
                    st.info(insight['message'])

        # 5. Export Options
        st.markdown("---")
        st.subheader("📥 Export Data")

        export_col1, export_col2 = st.columns([1, 3])

        with export_col1:
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with export_col2:
            if st.button("🗑️ Clear Session Data", use_container_width=True):
                st.session_state['history'] = []
                st.session_state['current_index'] = 0
                st.session_state['session_start_time'] = None
                st.rerun()

    else:
        st.info(
            "📭 No session data available. Start a live monitoring session in the 'Live Monitor' tab to generate a report.")
        st.markdown("""
        ### How to use:
        1. Go to the **🔴 Live Monitor** tab
        2. Click **▶️ Start Session** to begin monitoring
        3. Watch real-time physiological signals
        4. Click **⏸️ Stop Session** when complete
        5. Return here to view detailed analytics
        """)

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer-styled">
    AI-ReHaB Stress Analytics Platform &nbsp;|&nbsp; Powered by ML Physiological Inference
    &nbsp;|&nbsp; Random Forest Classifier &middot; 88% Accuracy
</div>
""", unsafe_allow_html=True)