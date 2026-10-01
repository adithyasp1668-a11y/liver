import csv
import joblib


MODEL_FILE = "mhe_demo_model.joblib"
INPUT_FILE = "breath_features.csv"


model = joblib.load(MODEL_FILE)


with open(INPUT_FILE, "r") as file:

    reader = csv.DictReader(file)

    print()
    print("======================================")
    print("       MHE DEMO PREDICTION")
    print("======================================")
    print()

    for row in reader:

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


        prediction = model.predict([features])[0]

        probability = model.predict_proba([features])[0]

        if prediction == 1:

            result = "MHE-LIKE PATTERN"

        else:

            result = "CONTROL-LIKE PATTERN"


        print(
            "Sample:",
            row["sample_id"]
        )

        print(
            "Prediction:",
            result
        )

        print(
            "Demo probability:",
            round(max(probability) * 100, 2),
            "%"
        )

        print("--------------------------------------")


print()
print("This is an experimental demonstration.")
print("It is NOT a medical diagnosis.")
