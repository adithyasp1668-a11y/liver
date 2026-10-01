import csv
import statistics

FILE = "mhe_sensor_data.csv"

mq135 = []
mq3 = []
mq4 = []

with open(FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:
            mq135.append(float(row["mq135"]))
            mq3.append(float(row["mq3"]))
            mq4.append(float(row["mq4"]))

        except:
            continue


print()
print("======================================")
print("       MQ SENSOR BASELINE")
print("======================================")

print(f"Number of samples: {len(mq135)}")

print()

print(f"MQ135 Mean : {statistics.mean(mq135):.2f}")
print(f"MQ135 Std  : {statistics.stdev(mq135):.2f}")

print()

print(f"MQ3 Mean   : {statistics.mean(mq3):.2f}")
print(f"MQ3 Std    : {statistics.stdev(mq3):.2f}")

print()

print(f"MQ4 Mean   : {statistics.mean(mq4):.2f}")
print(f"MQ4 Std    : {statistics.stdev(mq4):.2f}")

print()
print("======================================")
