import streamlit as st
import numpy as np
import joblib
import tensorflow as tf

# Load the model and scaler
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("model/model.keras")
    scaler = joblib.load("model/scaler.pkl")
    return model, scaler

model, scaler = load_model()

st.title("🏥 Health Risk Predictor")
st.markdown("Predict the likelihood of developing health risks using AI.")

# Define input fields
age = st.number_input("Age", min_value=0, max_value=120, value=30)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=24.5)
bp = st.number_input("Blood Pressure", min_value=50, max_value=200, value=120)
chol = st.number_input("Cholesterol", min_value=100, max_value=400, value=200)
glucose = st.number_input("Glucose", min_value=50, max_value=300, value=100)

if st.button("Predict Risk"):
    # Prepare features
    features = np.array([[age, bmi, bp, chol, glucose]])
    scaled = scaler.transform(features)
    pred = model.predict(scaled)
    risk = float(pred[0][0]) * 100

    st.subheader(f"🩺 Estimated Health Risk: **{risk:.2f}%**")
    if risk > 70:
        st.error("High risk! Please consult a doctor.")
    elif risk > 40:
        st.warning("Moderate risk. Consider lifestyle improvements.")
    else:
        st.success("Low risk! Keep maintaining healthy habits.")
