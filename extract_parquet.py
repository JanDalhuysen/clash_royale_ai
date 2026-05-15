import os
import io
import pandas as pd
from PIL import Image
from tqdm import tqdm

# Define paths
parquet_path = "arena7.parquet"  # Change to your Parquet file path
output_folder = "extracted_images2"  # The folder where images will save
image_column_name = "image.bytes"  # Change to your actual column name
image_format = "png"  # Extension to save as (e.g., png, jpg)

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the Parquet file
print("Loading Parquet file...")
df = pd.read_parquet(parquet_path, columns=[image_column_name])

# Loop through and save each image
print(f"Extracting images to '{output_folder}'...")
for index, row in enumerate(tqdm(df[image_column_name])):
    # Skip empty or null rows
    if pd.isna(row) or row is None:
        continue

    try:
        # Convert binary bytes to an image object
        image_bytes = bytes(row)
        image = Image.open(io.BytesIO(image_bytes))

        # Define unique filename (e.g., image_0.png, image_1.png)
        filename = f"image_{index}.{image_format}"
        file_path = os.path.join(output_folder, filename)

        # Save to disk
        image.save(file_path)
    except Exception as e:
        print(f"Error extracting row {index}: {e}")


print("Extraction complete")
