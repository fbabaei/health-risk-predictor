import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -----------------------------
# 1️⃣ Generate synthetic dataset
# -----------------------------
np.random.seed(42)
N = 1000

age = np.random.randint(20, 90, N)
bmi = np.random.uniform(18, 40, N)
blood_pressure = np.random.randint(80, 180, N)
glucose_level = np.random.randint(70, 250, N)
num_prev_visits = np.random.randint(0, 10, N)

# Risk score (fake target variable)
# Weighted combination + some noise
risk_score = (
    0.03 * age +
    0.05 * bmi +
    0.04 * blood_pressure +
    0.06 * glucose_level +
    0.1 * num_prev_visits +
    np.random.normal(0, 5, N)
)

df = pd.DataFrame({
    "age": age,
    "bmi": bmi,
    "blood_pressure": blood_pressure,
    "glucose_level": glucose_level,
    "num_prev_visits": num_prev_visits,
    "risk_score": risk_score
})

# -----------------------------
# 2️⃣ Split and preprocess
# -----------------------------
X = df.drop("risk_score", axis=1)
y = df["risk_score"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# -----------------------------
# 3️⃣ Build TensorFlow model
# -----------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1)  # Regression output
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# -----------------------------
# 4️⃣ Train
# -----------------------------
history = model.fit(X_train, y_train, validation_split=0.2, epochs=30, batch_size=16, verbose=1)

# -----------------------------
# 5️⃣ Save model & preprocessor
# -----------------------------
# Save model in TensorFlow directory format
model.save("model")

# Save the scaler for use in Streamlit app
import pickle
with open("model/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model and scaler saved successfully.")
