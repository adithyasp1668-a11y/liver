import serial
import csv
import time
import os

# =========================
# ESP32 SERIAL SETTINGS
# =========================

PORT = "/dev/ttyUSB0"
BAUD = 115200

# =========================
# YOUR BASELINE VALUES
# =========================

BASE_MQ135 = 659.30
BASE_MQ3   = 558.92
BASE_MQ4   = 516.05

# =========================
# OUTPUT FILE
# =========================

CSV_FILE = "breath_samples.csv"

# =========================
# SAMPLE ID
# =========================

sample_id = input("Enter sample ID (example B001): ").strip()

if sample_id == "":
    sample_id = "B001"


# =========================
# CONNECT ESP32
# =========================

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=2
)

time.sleep(2)


print()
print("==========================================")
print("       BREATH RESPONSE COLLECTION")
print("==========================================")

print("Sample ID :", sample_id)
print("ESP32     :", PORT)
print()

print("Baseline:")
print("MQ135 =", BASE_MQ135)
print("MQ3   =", BASE_MQ3)
print("MQ4   =", BASE_MQ4)

print()
print("Collection started...")
print("Press Ctrl+C to stop.")
print()


# =========================
# CREATE CSV
# =========================

file_exists = os.path.exists(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([
            "sample_id",
            "timestamp",
            "mq135",
            "mq3",
            "mq4",
            "mq135_change",
            "mq3_change",
            "mq4_change"
        ])


    # =========================
    # READ ESP32
    # =========================

    while True:

        try:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            # Ignore header
            if line.startswith("timestamp"):
                continue

            parts = line.split(",")

            if len(parts) != 4:
                continue

            timestamp = int(parts[0])

            mq135 = float(parts[1])
            mq3   = float(parts[2])
            mq4   = float(parts[3])


            # =========================
            # PERCENTAGE CHANGE
            # =========================

            change135 = (
                (mq135 - BASE_MQ135)
                / BASE_MQ135
            ) * 100

            change3 = (
                (mq3 - BASE_MQ3)
                / BASE_MQ3
            ) * 100

            change4 = (
                (mq4 - BASE_MQ4)
                / BASE_MQ4
            ) * 100


            # =========================
            # SAVE
            # =========================

            writer.writerow([
                sample_id,
                timestamp,
                round(mq135, 2),
                round(mq3, 2),
                round(mq4, 2),
                round(change135, 2),
                round(change3, 2),
                round(change4, 2)
            ])

            file.flush()


            # =========================
            # DISPLAY
            # =========================

            print(
                f"{sample_id} | "
                f"MQ135: {mq135:.1f} "
                f"({change135:+.2f}%) | "
                f"MQ3: {mq3:.1f} "
                f"({change3:+.2f}%) | "
                f"MQ4: {mq4:.1f} "
                f"({change4:+.2f}%)"
            )


        except KeyboardInterrupt:

            print()
            print("Collection stopped.")
            break


        except Exception as e:

            print("Error:", e)


ser.close()
