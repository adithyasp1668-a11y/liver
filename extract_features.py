import csv
import math
from collections import defaultdict

INPUT_FILE = "breath_samples.csv"
OUTPUT_FILE = "breath_features.csv"


def mean(values):
    return sum(values) / len(values)


def std(values):
    if len(values) < 2:
        return 0.0

    m = mean(values)

    return math.sqrt(
        sum((x - m) ** 2 for x in values)
        / (len(values) - 1)
    )


def slope(times, values):

    if len(values) < 2:
        return 0.0

    t_mean = mean(times)
    v_mean = mean(values)

    numerator = sum(
        (t - t_mean) * (v - v_mean)
        for t, v in zip(times, values)
    )

    denominator = sum(
        (t - t_mean) ** 2
        for t in times
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ==========================================
# READ DATA
# ==========================================

samples = defaultdict(list)

with open(INPUT_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:

            sample_id = row["sample_id"]

            timestamp = float(row["timestamp"])

            mq135 = float(row["mq135"])
            mq3 = float(row["mq3"])
            mq4 = float(row["mq4"])

            samples[sample_id].append(
                (timestamp, mq135, mq3, mq4)
            )

        except Exception:
            continue


# ==========================================
# FEATURE EXTRACTION
# ==========================================

features = []


for sample_id, rows in samples.items():

    if len(rows) < 5:
        continue

    times = [r[0] for r in rows]

    mq135 = [r[1] for r in rows]
    mq3   = [r[2] for r in rows]
    mq4   = [r[3] for r in rows]


    # --------------------------------------
    # MQ135
    # --------------------------------------

    mq135_mean = mean(mq135)
    mq135_min = min(mq135)
    mq135_max = max(mq135)
    mq135_std = std(mq135)

    mq135_range = mq135_max - mq135_min

    mq135_response = (
        (mq135_max - mq135[0])
        / mq135[0]
    ) * 100


    mq135_slope = slope(
        times,
        mq135
    )


    # --------------------------------------
    # MQ3
    # --------------------------------------

    mq3_mean = mean(mq3)
    mq3_min = min(mq3)
    mq3_max = max(mq3)
    mq3_std = std(mq3)

    mq3_range = mq3_max - mq3_min

    mq3_response = (
        (mq3_max - mq3[0])
        / mq3[0]
    ) * 100


    mq3_slope = slope(
        times,
        mq3
    )


    # --------------------------------------
    # MQ4
    # --------------------------------------

    mq4_mean = mean(mq4)
    mq4_min = min(mq4)
    mq4_max = max(mq4)
    mq4_std = std(mq4)

    mq4_range = mq4_max - mq4_min

    mq4_response = (
        (mq4_max - mq4[0])
        / mq4[0]
    ) * 100


    mq4_slope = slope(
        times,
        mq4
    )


    # --------------------------------------
    # STORE FEATURES
    # --------------------------------------

    features.append([
        sample_id,

        mq135_mean,
        mq135_min,
        mq135_max,
        mq135_std,
        mq135_range,
        mq135_response,
        mq135_slope,

        mq3_mean,
        mq3_min,
        mq3_max,
        mq3_std,
        mq3_range,
        mq3_response,
        mq3_slope,

        mq4_mean,
        mq4_min,
        mq4_max,
        mq4_std,
        mq4_range,
        mq4_response,
        mq4_slope,

        len(rows)
    ])


# ==========================================
# SAVE FEATURE FILE
# ==========================================

headers = [

    "sample_id",

    "mq135_mean",
    "mq135_min",
    "mq135_max",
    "mq135_std",
    "mq135_range",
    "mq135_response",
    "mq135_slope",

    "mq3_mean",
    "mq3_min",
    "mq3_max",
    "mq3_std",
    "mq3_range",
    "mq3_response",
    "mq3_slope",

    "mq4_mean",
    "mq4_min",
    "mq4_max",
    "mq4_std",
    "mq4_range",
    "mq4_response",
    "mq4_slope",

    "num_readings"
]


with open(
    OUTPUT_FILE,
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow(headers)

    for row in features:

        writer.writerow([
            row[0]
        ] + [
            round(x, 4)
            for x in row[1:]
        ])


print()
print("======================================")
print("       FEATURE EXTRACTION")
print("======================================")

print("Input :", INPUT_FILE)
print("Output:", OUTPUT_FILE)

print()

print("Samples processed:", len(features))

print()

for row in features:

    print(
        "Sample:",
        row[0],
        "| Readings:",
        row[-1]
    )

print()
print("Feature extraction complete.")
