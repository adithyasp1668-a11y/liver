import csv

INPUT_FILE = "breath_features.csv"
OUTPUT_FILE = "mhe_dataset.csv"

with open(INPUT_FILE, "r") as infile:

    reader = csv.DictReader(infile)

    rows = list(reader)
    headers = reader.fieldnames


# Current samples are from normal/control people
for row in rows:
    row["label"] = 0


headers.append("label")


with open(OUTPUT_FILE, "w", newline="") as outfile:

    writer = csv.DictWriter(
        outfile,
        fieldnames=headers
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print("===================================")
print("      MHE DATASET PREPARATION")
print("===================================")

print("Samples:", len(rows))
print("CONTROL samples:", len(rows))
print("MHE samples: 0")

print()
print("Saved as:", OUTPUT_FILE)
print()
print("Dataset is ready for adding real MHE samples.")
