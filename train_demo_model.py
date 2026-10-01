import csv
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


INPUT_FILE = "mhe_demo_dataset.csv"
MODEL_FILE = "mhe_demo_model.joblib"


# =====================================================
# READ DATA
# =====================================================

X = []
y = []

with open(INPUT_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        # Do NOT use sample ID as a feature
        # Do NOT use label as a feature

        features = [
            float(row["mq135_mean"]),
            float(row["mq135_min"]),
            float(row["mq135_max"]),
            float(row["mq135_std"]),
            float(row["mq135_range"]),
            float(row["mq135_response"]),
            float(row["mq135_slope"]),

            float(row["mq3_mean"]),
            float(row["mq3_min"]),
            float(row["mq3_max"]),
            float(row["mq3_std"]),
            float(row["mq3_range"]),
            float(row["mq3_response"]),
            float(row["mq3_slope"]),

            float(row["mq4_mean"]),
            float(row["mq4_min"]),
            float(row["mq4_max"]),
            float(row["mq4_std"]),
            float(row["mq4_range"]),
            float(row["mq4_response"]),
            float(row["mq4_slope"]),

            float(row["num_readings"])
        ]

        X.append(features)
        y.append(int(row["label"]))


# =====================================================
# CHECK DATA
# =====================================================

control_count = y.count(0)
mhe_count = y.count(1)

print()
print("======================================")
print("       MHE DEMO AI TRAINING")
print("======================================")

print()
print("Total samples :", len(X))
print("CONTROL       :", control_count)
print("SYNTHETIC MHE :", mhe_count)

print()


# =====================================================
# CREATE MODEL
# =====================================================

model = Pipeline([

    (
        "scaler",
        StandardScaler()
    ),

    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        )
    )
])


# =====================================================
# TRAIN
# =====================================================

print("Training model...")

model.fit(X, y)

print("Training complete.")


# =====================================================
# SAVE
# =====================================================

joblib.dump(model, MODEL_FILE)

print()
print("Model saved as:")
print(MODEL_FILE)

print()
print("======================================")
print("IMPORTANT")
print("======================================")
print("This is a SYNTHETIC DEMONSTRATION MODEL.")
print("It is NOT clinically validated.")
print("Do not report its training performance")
print("as medical diagnostic accuracy.")
print()
