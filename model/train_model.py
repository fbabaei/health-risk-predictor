import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# Create sample patient data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    "age": np.random.randint(20, 80, n),
    "bmi": np.random.uniform(18, 35, n),
    "blood_pressure": np.random.randint(90, 160, n),
    "cholesterol": np.random.randint(150, 280, n),
    "glucose": np.random.randint(70, 160, n),
})
data["risk_score"] = (
    0.3 * data["age"] +
    0.2 * data["bmi"] +
    0.25 * data["blood_pressure"] +
    0.15 * data["cholesterol"] +
    0.1 * data["glucose"]
) / 10 + np.random.normal(0, 1, n)

# Save sample data
os.makedirs("data", exist_ok=True)
data.to_csv("data/patients.csv", index=False)

# Split and normalize
X = data[["age", "bmi", "blood_pressure", "cholesterol", "glucose"]]
y = data["risk_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build TensorFlow model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer="adam", loss="mse")

# Train model
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=0)

# Save model
os.makedirs("model", exist_ok=True)
model.save("model/")

# Save scaler for use in app
import joblib
joblib.dump(scaler, "model/scaler.pkl")

print("✅ Model and scaler saved successfully.")
