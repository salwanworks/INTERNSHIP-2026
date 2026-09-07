import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

# SNR data
snr = np.array([
    10, 12, 11, 13, 14,
    15, 13, 16, 17, 18,
    16, 19, 20, 18, 21,
    22, 20, 23, 24, 25
], dtype=float)

# Normalize the data
minimum = snr.min()
maximum = snr.max()

snr_normalized = (snr - minimum) / (maximum - minimum)

# Window size
window = 5

# Create input and output windows
X = []
y = []

for i in range(len(snr_normalized) - window):
    X.append(snr_normalized[i:i + window])
    y.append(snr_normalized[i + window])

X = np.array(X).reshape(-1, window, 1)
y = np.array(y)

# RNN model
model = Sequential([
    SimpleRNN(10, input_shape=(window, 1)),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")

# Train
model.fit(X, y, epochs=200, verbose=0)

# Predict the next value
prediction = model.predict(X[-1:], verbose=0)[0][0]

# Convert prediction back to original SNR scale
prediction = prediction * (maximum - minimum) + minimum

print("Last 5 SNR values:", snr[-6:-1])
print("Actual next value:", snr[-1])
print("Predicted next value:", prediction)
