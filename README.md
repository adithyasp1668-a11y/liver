# 🫁 AI-Based Minimal Hepatic Encephalopathy (MHE) Detection in Liver Cirrhosis

An AI-assisted breath analysis system designed to support the early detection and screening of **Minimal Hepatic Encephalopathy (MHE)** in patients with liver cirrhosis using breath-sensor data and machine learning.

---

## 📌 Overview

Liver cirrhosis can lead to complications such as **Hepatic Encephalopathy (HE)**. Minimal Hepatic Encephalopathy (MHE) is an early stage in which patients may not show obvious clinical symptoms, but subtle neurological and cognitive changes can already be present.

This project explores a **non-invasive breath-analysis approach** for detecting patterns associated with MHE.

The system combines:

- 🌬️ Breath sensing
- 🔬 Gas-sensor measurements
- 🌡️ Temperature and humidity monitoring
- 📊 Sensor-data preprocessing
- 🤖 Machine Learning
- 🖥️ Real-time monitoring dashboard

The prototype processes breath-sensor measurements and uses a trained machine-learning model to classify the input into an MHE-related prediction category.

> **Important:** This is a research/prototype system and is not intended to replace clinical diagnosis, laboratory testing, or medical evaluation.

---

# 🎯 Objectives

The main objectives of this project are:

1. Develop a low-cost breath-analysis prototype.
2. Capture multiple characteristics of exhaled breath.
3. Preprocess and extract useful features from sensor readings.
4. Develop a machine-learning model for MHE-related classification.
5. Provide a real-time demonstration of the prediction pipeline.
6. Display sensor readings and AI results through a dashboard.
7. Explore the feasibility of non-invasive screening support for MHE.

---

# 🧠 System Concept

The proposed system follows this pipeline:

```text
          Patient Breath
                │
                ▼
       ┌─────────────────┐
       │  Breath Chamber │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Gas Sensors     │
       │ MQ135 / MQ3 /   │
       │ MQ4             │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Sensor Data      │
       │ Acquisition      │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Data Processing  │
       │ & Feature        │
       │ Extraction       │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Machine Learning │
       │ Model            │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ MHE Prediction   │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Dashboard        │
       │ Visualization    │
       └─────────────────┘

🔬 Hardware
The prototype uses the following hardware components:
Component	Purpose
ESP32	Sensor data acquisition and communication
MQ135	Gas sensing
MQ3	Gas sensing
MQ4	Gas sensing
SHT31	Temperature and humidity measurement
Breath Chamber	Controlled breath-sample collection
Raspberry Pi 4	Data processing, ML inference and dashboard
ADS1262 (optional/extended setup)	High-resolution analog data acquisition

💻 Software
Programming
- Python
- C/C++ for microcontroller development
Python Libraries
- NumPy
- Pandas
- Scikit-learn
- Joblib
- Matplotlib
Hardware / Data Processing
- ESP32
- Raspberry Pi
- Serial communication
- CSV-based data processing
Machine Learning
The project uses machine-learning techniques to process sensor features and generate an MHE-related prediction.
The trained model is stored as:
mhe_demo_model.joblib

🤖 Machine Learning Pipeline
The machine-learning workflow consists of the following stages:
Raw Sensor Data
       │
       ▼
Data Cleaning
       │
       ▼
Preprocessing
       │
       ▼
Feature Extraction
       │
       ▼
Feature Scaling / Transformation
       │
       ▼
Machine Learning Model
       │
       ▼
Prediction
       │
       ▼
Dashboard Result

The project contains scripts for:
- Dataset preparation
- Feature extraction
- Model training
- Model testing
- Demo-data generation
- Real-time prediction

📂 Project Structure
liver/
│
├── live_mhe_demo.py
│       Main MHE demonstration and prediction program
│
├── dashboard.py
│       Dashboard application
│
├── dashboard_data.json
│       Data used by the dashboard
│
├── collect_breath.py
│       Breath-sample collection
│
├── receive_sensor.py
│       Sensor-data reception
│
├── calculate_baseline.py
│       Sensor baseline calculation
│
├── extract_features.py
│       Feature extraction from sensor data
│
├── prepare_dataset.py
│       Dataset preprocessing and preparation
│
├── train_demo_model.py
│       Machine-learning model training
│
├── test_mhe_model.py
│       Model testing
│
├── create_demo_data.py
│       Demo-data generation
│
├── mhe_demo_model.joblib
│       Trained machine-learning model
│
├── breath_samples.csv
│       Breath sample data
│
├── breath_features.csv
│       Extracted breath features
│
├── mhe_dataset.csv
│       MHE-related dataset
│
├── mhe_demo_dataset.csv
│       Demonstration dataset
│
├── mhe_sensor_data.csv
│       Sensor measurements
│
└── README.md
