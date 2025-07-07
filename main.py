import os
import logging
from converter import convert_mp4_to_gif, convert_webp_to_gif

# Setup logging
logging.basicConfig(
    filename='conversion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting conversion process.")

# Default folders
input_folder = "input_videos"
output_folder = "output_gifs"

# Ensure folders exist
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Get files
files = os.listdir(input_folder)
valid_files = [f for f in files if os.path.isfile(os.path.join(input_folder, f))]

if not valid_files:
    logging.warning("No files found in input folder.")
else:
    count = 1
    num_digits = len(str(len(valid_files)))
    prefix = "newgif"

    for file in valid_files:
        ext = file.lower().split(".")[-1]
        input_path = os.path.join(input_folder, file)
        output_name = f"{prefix}{str(count).zfill(num_digits)}.gif"
        output_path = os.path.join(output_folder, output_name)

        try:
            if ext == "mp4":
                convert_mp4_to_gif(input_path, output_path)
                logging.info(f"Converted MP4: {file} -> {output_name}")
            elif ext == "webp":
                convert_webp_to_gif(input_path, output_path)
                logging.info(f"Converted WEBP: {file} -> {output_name}")
            else:
                logging.info(f"Unsupported file type: {file}")
        except Exception as e:
            logging.error(f"Failed to convert {file}: {e}")
        
        count += 1

logging.info("All tasks completed.")
