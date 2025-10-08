import os
os.environ["STREAMLIT_HOME"] = os.path.join(os.getcwd(), ".streamlit")

import streamlit as st
import tensorflow as tf
import numpy as np
import pickle

# Load model & scaler
model = tf.keras.models.load_model("model/model.keras")
with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

st.title("🏥 Health Risk Predictor")

# Inputs
age = st.number_input("Age", min_value=0, max_value=120, value=45)
bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
bp = st.number_input("Blood Pressure", min_value=60, max_value=180, value=120)
glucose = st.number_input("Glucose Level", min_value=50, max_value=300, value=100)
visits = st.number_input("Number of Previous Visits", min_value=0, max_value=50, value=2)

if st.button("Predict Risk"):
    X = np.array([[age, bmi, bp, glucose, visits]])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)
    st.success(f"Predicted Readmission Risk: {pred[0][0]:.2f}")
