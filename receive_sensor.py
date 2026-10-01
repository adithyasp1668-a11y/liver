import serial
import csv
import time
import os

PORT = "/dev/ttyUSB0"
BAUD = 115200

CSV_FILE = "mhe_sensor_data.csv"

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=2
)

time.sleep(2)

print("===================================")
print("   MHE SENSOR DATA COLLECTOR")
print("===================================")
print("ESP32 connected:", PORT)
print("Saving data to:", CSV_FILE)
print()

file_exists = os.path.exists(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "mq135",
            "mq3",
            "mq4"
        ])

    while True:

        try:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            print("ESP32:", line)

            # Ignore ESP32 header
            if line.startswith("timestamp"):
                continue

            parts = line.split(",")

            if len(parts) != 4:
                continue

            timestamp = parts[0]
            mq135 = parts[1]
            mq3 = parts[2]
            mq4 = parts[3]

            writer.writerow([
                timestamp,
                mq135,
                mq3,
                mq4
            ])

            file.flush()

        except KeyboardInterrupt:

            print("\nStopping...")
            break

        except Exception as e:

            print("Error:", e)

ser.close()
