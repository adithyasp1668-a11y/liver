import serial
import time
import statistics
import joblib
import json
from datetime import datetime


# ==========================================
# SETTINGS
# ==========================================

PORT = "/dev/ttyUSB0"
BAUD = 115200

COLLECTION_TIME = 60

MODEL_FILE = "mhe_demo_model.joblib"
DASHBOARD_FILE = "dashboard_data.json"


# ==========================================
# LOAD MODEL
# ==========================================

try:
    model = joblib.load(MODEL_FILE)
except Exception as e:
    print("ERROR: Could not load AI model.")
    print(e)
    exit()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calc_mean(values):

    return sum(values) / len(values)


def calc_std(values):

    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


def calc_slope(times, values):

    if len(values) < 2:
        return 0.0

    t_mean = calc_mean(times)
    v_mean = calc_mean(values)

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
# FEATURE EXTRACTION
# ==========================================

def make_features(times, mq135, mq3, mq4):

    features = []

    for values in [mq135, mq3, mq4]:

        avg = calc_mean(values)
        minimum = min(values)
        maximum = max(values)
        sd = calc_std(values)

        value_range = maximum - minimum

        if values[0] != 0:

            response = (
                (maximum - values[0])
                / values[0]
            ) * 100

        else:

            response = 0.0

        sl = calc_slope(times, values)

        features.extend([
            avg,
            minimum,
            maximum,
            sd,
            value_range,
            response,
            sl
        ])

    features.append(len(mq135))

    return features


# ==========================================
# UPDATE DASHBOARD
# ==========================================

def update_dashboard(
    mq135,
    mq3,
    mq4,
    score,
    result,
    readings
):

    data = {

        "mq135": round(mq135, 2),

        "mq3": round(mq3, 2),

        "mq4": round(mq4, 2),

        "score": round(score, 1),

        "result": result,

        "readings": readings,

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    try:

        with open(
            DASHBOARD_FILE,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        print()
        print("Dashboard updated successfully.")

    except Exception as e:

        print()
        print("WARNING: Could not update dashboard.")
        print(e)


# ==========================================
# START SYSTEM
# ==========================================

print()
print("======================================")
print("       LIVE MHE DEMO SYSTEM")
print("======================================")
print()

print("Loading AI model...")
print("Model loaded successfully.")
print()

print("Connecting to ESP32...")


# ==========================================
# CONNECT ESP32
# ==========================================

try:

    ser = serial.Serial(
        PORT,
        BAUD,
        timeout=1
    )

except Exception as e:

    print()
    print("ERROR: Could not connect to ESP32.")
    print("Port:", PORT)
    print(e)
    exit()


time.sleep(2)

print()
print("ESP32 connected:", PORT)
print()


# ==========================================
# BREATH COLLECTION
# ==========================================

print("======================================")
print("        BREATH COLLECTION")
print("======================================")
print()

print("Keep the breath chamber ready.")
print("Start breathing normally into the chamber.")
print()

print(
    "Collecting for",
    COLLECTION_TIME,
    "seconds..."
)

print()


# ==========================================
# DATA ARRAYS
# ==========================================

times = []

mq135_values = []
mq3_values = []
mq4_values = []

start = time.time()


# ==========================================
# READ ESP32
# ==========================================

while time.time() - start < COLLECTION_TIME:

    line = ser.readline().decode(
        "utf-8",
        errors="ignore"
    ).strip()

    if not line:
        continue

    print("ESP32:", line)

    # Expected:
    # timestamp,mq135,mq3,mq4

    parts = line.split(",")

    if len(parts) != 4:
        continue

    try:

        timestamp = float(parts[0])

        mq135 = float(parts[1])

        mq3 = float(parts[2])

        mq4 = float(parts[3])

    except ValueError:

        continue

    times.append(timestamp)

    mq135_values.append(mq135)

    mq3_values.append(mq3)

    mq4_values.append(mq4)


# ==========================================
# CLOSE SERIAL
# ==========================================

ser.close()


# ==========================================
# CHECK DATA
# ==========================================

print()
print("======================================")
print("       COLLECTION COMPLETE")
print("======================================")
print()

print(
    "Readings collected:",
    len(mq135_values)
)


if len(mq135_values) < 20:

    print()
    print("ERROR: Not enough valid sensor readings.")
    print()
    print("Check:")
    print("1. ESP32 USB connection")
    print("2. ESP32 serial output")
    print("3. Baud rate = 115200")
    print("4. Serial format = timestamp,mq135,mq3,mq4")
    print()

    exit()


# ==========================================
# FEATURE EXTRACTION
# ==========================================

features = make_features(
    times,
    mq135_values,
    mq3_values,
    mq4_values
)

print()
print("Feature extraction complete.")
print()


# ==========================================
# AI PREDICTION
# ==========================================

try:

    prediction = model.predict(
        [features]
    )[0]

    probabilities = model.predict_proba(
        [features]
    )[0]

    demo_score = max(probabilities) * 100

except Exception as e:

    print("ERROR during AI prediction.")
    print(e)
    exit()


# ==========================================
# SENSOR MEANS
# ==========================================

mq135_mean = calc_mean(
    mq135_values
)

mq3_mean = calc_mean(
    mq3_values
)

mq4_mean = calc_mean(
    mq4_values
)


# ==========================================
# RESULT
# ==========================================

if prediction == 1:

    result = "NO MHE DETECTED"

else:

    result = "MHE DETECTED"


# ==========================================
# DISPLAY RESULT
# ==========================================

print()
print("======================================")
print("          AI DEMO RESULT")
print("======================================")
print()

print(
    "MQ135 mean:",
    round(mq135_mean, 2)
)

print(
    "MQ3 mean  :",
    round(mq3_mean, 2)
)

print(
    "MQ4 mean  :",
    round(mq4_mean, 2)
)

print()

print("RESULT:")
print(result)

print()

print(
    "Demo model score:",
    round(demo_score, 2),
    "%"
)

print()


# ==========================================
# UPDATE DASHBOARD
# ==========================================

update_dashboard(

    mq135_mean,

    mq3_mean,

    mq4_mean,

    demo_score,

    result,

    len(mq135_values)
)


# ==========================================
# IMPORTANT MESSAGE
# ==========================================

print()
print("======================================")
print("             IMPORTANT")
print("======================================")

print(
    "This is an experimental SIH prototype."
)

print(
    "The model uses SYNTHETIC MHE demonstration data."
)

print(
    "It is NOT clinically validated."
)

print(
    "The result must NOT be used as a medical diagnosis."
)

print()
print("Test complete.")
print()
