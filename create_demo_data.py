import csv
import random

INPUT_FILE = "mhe_dataset.csv"
OUTPUT_FILE = "mhe_demo_dataset.csv"

# Read existing CONTROL data
with open(INPUT_FILE, "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    headers = reader.fieldnames

# Keep only your real CONTROL samples
control_rows = []

for row in rows:
    if row["label"] == "0":
        control_rows.append(row)

# Create synthetic MHE-like demonstration samples
demo_rows = []

random.seed(42)

numeric_columns = [
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
    "mq4_slope"
]

for i in range(30):

    # Pick one real CONTROL sample as a starting point
    base = random.choice(control_rows)

    new_row = {}

    # Synthetic sample ID
    new_row["sample_id"] = "SYN_MHE_%02d" % (i + 1)

    for column in numeric_columns:

        value = float(base[column])

        # Create a synthetic sensor-response shift
        factor = random.uniform(1.15, 1.45)

        noise = random.uniform(-0.05, 0.05)

        new_value = value * factor * (1 + noise)

        # Prevent negative values
        if new_value < 0:
            new_value = 0

        new_row[column] = round(new_value, 4)

    new_row["num_readings"] = random.randint(180, 230)

    # 1 = synthetic MHE demonstration class
    new_row["label"] = "1"

    demo_rows.append(new_row)


# Combine real controls + synthetic demo samples
all_rows = control_rows + demo_rows

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=headers
    )

    writer.writeheader()
    writer.writerows(all_rows)


print()
print("======================================")
print(" SYNTHETIC MHE DEMO DATASET")
print("======================================")
print()
print("Real CONTROL samples :", len(control_rows))
print("Synthetic MHE samples:", len(demo_rows))
print("Total samples        :", len(all_rows))
print()
print("Saved as:", OUTPUT_FILE)
print()
print("IMPORTANT:")
print("MHE samples are SYNTHETIC demonstration data.")
print("They are NOT real patient measurements.")
