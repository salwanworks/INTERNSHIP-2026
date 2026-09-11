import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, classification_report

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("dataset.csv")

print("===================================")
print("SATELLITE DATASET")
print("===================================")

print("Total rows    :", len(df))
print("Total columns :", len(df.columns))


# ============================================================
# 2. SELECT 19 FEATURES
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

# Ground-truth labels
y = df["anomaly"]

# Handle missing values
X = X.fillna(X.median())


# ============================================================
# 3. SPLIT DATASET: 80% TRAINING, 20% TESTING
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n===================================")
print("DATASET SPLIT")
print("===================================")

print("Total records    :", len(df))
print("Training records :", len(X_train))
print("Testing records  :", len(X_test))


# ============================================================
# 4. CREATE ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)


# ============================================================
# 5. TRAIN MODEL ONLY ON TRAINING DATA
# ============================================================

model.fit(X_train)


# ============================================================
# 6. PREDICT ONLY THE UNSEEN TEST DATA
# ============================================================

prediction = model.predict(X_test)


# ============================================================
# 7. CONVERT ISOLATION FOREST OUTPUT
# ============================================================

# Isolation Forest:
#  1  = NORMAL
# -1  = ANOMALY

predicted_binary = pd.Series(prediction).map({
    1: 0,
    -1: 1
})


# ============================================================
# 8. ANOMALY SCORE
# ============================================================

anomaly_score = model.decision_function(X_test)


# ============================================================
# 9. DISPLAY TEST RESULTS
# ============================================================

result = df.loc[X_test.index].copy()

result["Prediction"] = prediction

result["Status"] = result["Prediction"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})

result["AnomalyScore"] = anomaly_score


print("\n===================================")
print("TEST DATA RESULTS")
print("===================================")

print(
    result[
        [
            "segment",
            "anomaly",
            "Prediction",
            "Status",
            "AnomalyScore"
        ]
    ].head(20)
)


# ============================================================
# 10. MODEL SUMMARY
# ============================================================

normal_count = (prediction == 1).sum()
anomaly_count = (prediction == -1).sum()

print("\n===================================")
print("MODEL SUMMARY")
print("===================================")

print("Predicted NORMAL records :", normal_count)
print("Predicted ANOMALY records:", anomaly_count)

print("\nActual NORMAL records    :", (y_test == 0).sum())
print("Actual ANOMALY records   :", (y_test == 1).sum())


# ============================================================
# 11. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    predicted_binary
)

print("\n===================================")
print("CONFUSION MATRIX")
print("===================================")

print(cm)


# ============================================================
# 12. CLASSIFICATION REPORT
# ============================================================

print("\n===================================")
print("CLASSIFICATION REPORT")
print("===================================")

print(
    classification_report(
        y_test,
        predicted_binary,
        target_names=["NORMAL", "ANOMALY"]
    )
)


# ============================================================
# 13. FIRST 20 DETECTED ANOMALIES
# ============================================================

print("\n===================================")
print("FIRST 20 DETECTED ANOMALIES")
print("===================================")

print(
    result[
        result["Prediction"] == -1
    ][
        [
            "segment",
            "anomaly",
            "Prediction",
            "AnomalyScore"
        ]
    ].head(20)
)
