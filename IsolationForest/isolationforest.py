import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, classification_report

# ============================================================
# 1. LOAD SATELLITE DATASET
# ============================================================

df = pd.read_csv("satellite_dataset.csv")

print("===================================")
print("SATELLITE DATASET")
print("===================================")

print("Number of rows   :", len(df))
print("Number of columns:", len(df.columns))


# ============================================================
# 2. DEFINE TELEMETRY FEATURES
# ============================================================

features = [
    "sampling",
    "duration",
    "len",
    "mean",
    "var",
    "std",
    "kurtosis",
    "skew",
    "n_peaks",
    "smooth10_n_peaks",
    "smooth20_n_peaks",
    "diff_peaks",
    "diff2_peaks",
    "diff_var",
    "diff2_var",
    "gaps_squared",
    "len_weighted",
    "var_div_duration",
    "var_div_len"
]

X = df[features]


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

X = X.fillna(X.median())


print("\nNumber of features used:", len(features))

print("\nFeatures used:")
for feature in features:
    print("-", feature)


# ============================================================
# 4. CREATE ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)


# ============================================================
# 5. TRAIN ISOLATION FOREST
# ============================================================

model.fit(X)


# ============================================================
# 6. PREDICT ANOMALIES
# ============================================================

prediction = model.predict(X)


# ============================================================
# 7. STORE RESULTS
# ============================================================

result = df.copy()

result["Prediction"] = prediction

result["Status"] = result["Prediction"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})


# ============================================================
# 8. ANOMALY SCORE
# ============================================================

result["AnomalyScore"] = model.decision_function(X)


# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\n===================================")
print("ISOLATION FOREST RESULTS")
print("===================================")

print(
    result[
        ["segment", "anomaly", "Prediction",
         "Status", "AnomalyScore"]
    ].head(20)
)


# ============================================================
# 10. COUNT PREDICTIONS
# ============================================================

normal_count = (result["Prediction"] == 1).sum()
anomaly_count = (result["Prediction"] == -1).sum()

print("\n===================================")
print("MODEL SUMMARY")
print("===================================")

print("Predicted NORMAL records :", normal_count)
print("Predicted ANOMALY records:", anomaly_count)


# ============================================================
# 11. ACTUAL ANOMALIES IN DATASET
# ============================================================

actual_anomalies = (result["anomaly"] == 1).sum()
actual_normal = (result["anomaly"] == 0).sum()

print("\n===================================")
print("ACTUAL DATASET LABELS")
print("===================================")

print("Actual NORMAL records :", actual_normal)
print("Actual ANOMALY records:", actual_anomalies)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

# Convert:
# Actual: 0 = Normal, 1 = Anomaly
# Prediction: -1 = Anomaly, 1 = Normal

predicted_binary = result["Prediction"].map({
    1: 0,
    -1: 1
})

actual_binary = result["anomaly"]


cm = confusion_matrix(
    actual_binary,
    predicted_binary
)

print("\n===================================")
print("CONFUSION MATRIX")
print("===================================")

print(cm)


# ============================================================
# 13. CLASSIFICATION REPORT
# ============================================================

print("\n===================================")
print("CLASSIFICATION REPORT")
print("===================================")

print(
    classification_report(
        actual_binary,
        predicted_binary,
        target_names=["NORMAL", "ANOMALY"]
    )
)


# ============================================================
# 14. SHOW DETECTED ANOMALIES
# ============================================================

print("\n===================================")
print("FIRST 20 DETECTED ANOMALIES")
print("===================================")

print(
    result[
        result["Prediction"] == -1
    ][
        ["segment", "anomaly",
         "Prediction", "AnomalyScore"]
    ].head(20)
)
