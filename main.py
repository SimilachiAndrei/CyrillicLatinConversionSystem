import easyocr
import csv
from pathlib import Path

reader = easyocr.Reader(['ru'])  # Russian model for Cyrillic
cutouts_dir = Path("./cutouts")
metadata = []

# Read metadata
with open(cutouts_dir / "metadata.csv") as f:
    reader_csv = csv.DictReader(f)
    for row in reader_csv:
        metadata.append(row)

# OCR each cutout
with open("ocr_output.csv", "w") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["cutout_path", "cyrillic_text"])

    for row in metadata:
        img_path = cutouts_dir / row["window_name"]
        result = reader.readtext(str(img_path), detail=0)
        writer.writerow([str(img_path), " ".join(result)])