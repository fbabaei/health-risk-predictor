import streamlit as st
import tensorflow as tf
import joblib
import numpy as np

st.set_page_config(page_title="Patient Risk Score", page_icon="🩺", layout="centered")

st.title("🩺 Patient Risk Score Predictor")

# Load TensorFlow model and scaler
model = tf.keras.models.load_model("model/model.h5")
scaler = joblib.load("model/scaler.pkl")

st.sidebar.header("Enter Patient Data")

age = st.sidebar.slider("Age", 20, 80, 40)
bmi = st.sidebar.slider("BMI", 18.0, 35.0, 25.0)
bp = st.sidebar.slider("Blood Pressure", 90, 160, 120)
cholesterol = st.sidebar.slider("Cholesterol", 150, 280, 200)
glucose = st.sidebar.slider("Glucose", 70, 160, 100)

if st.button("Predict Risk Score"):
    X = np.array([[age, bmi, bp, cholesterol, glucose]])
    X_scaled = scaler.transform(X)
    risk_score = model.predict(X_scaled)[0][0]
    st.success(f"Predicted Risk Score: **{risk_score:.2f}**")

st.markdown("---")
st.caption("Model trained with synthetic data for demonstration.")
