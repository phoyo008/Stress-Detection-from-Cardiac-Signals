# Stress-Detection-from-Cardiac-Signals
A system that identifies stress markers in heart rate data using machine learning.
AI-ReHaB Stress Analytics
Real-Time Physiological Monitoring & Stress Detection System

This project is a machine learning-powered application designed to detect physiological stress states in real-time. It analyzes Heart Rate Variability (HRV) metrics to classify a user's condition into No Stress, Interruption, or Time Pressure.

Developed as a proof-of-concept for the AI-Driven Resilient Health and Biological Systems initiative, this tool demonstrates the fusion of biomedical signal processing, machine learning, and user-centric software design.

🚀 Project Overview
The application simulates a bio-monitoring dashboard that processes physiological data streams. It uses a Random Forest Classifier trained on the SWELL dataset to interpret cardiac signals and provide immediate, actionable feedback on mental fatigue and cognitive load.

Key Features
Live Monitoring Simulation: Streams physiological data at 1Hz to mimic real-time sensor input.

Dual-Axis Visualization: Plots Heart Rate (HR) against Heart Rate Variability (RMSSD) to visualize the inverse relationship during stress events.

Real-Time Classification: Instantly categorizes the user's state with 88% accuracy.

Clinical Session Reports: Generates post-session analytics, including stress load percentages and warnings when HRV drops significantly (>20%) from baseline.

🧠 The Science (Physiological Biomarkers)
This project focuses on specific features derived from cardiac signals to ensure clinical relevance:

RMSSD (Root Mean Square of Successive Differences): The primary time-domain measure of Heart Rate Variability. It reflects parasympathetic (vagal) activity; a drop in RMSSD indicates stress or high cognitive load.

LF/HF Ratio: The ratio of Low Frequency to High Frequency power. An elevated ratio signals sympathetic nervous system dominance (fight-or-flight response).

Mean RR: The average interval between heartbeats, used to establish a physiological baseline.

🛠️ Technical Architecture
Frontend: Streamlit (Python) for the interactive web interface.

Machine Learning: Scikit-learn (Random Forest Classifier, n_estimators=100).

Data Visualization: Plotly Express & Graph Objects for dynamic charting.

Data Processing: Pandas for feature engineering (HR, MEAN_RR, RMSSD, LF/HF).
