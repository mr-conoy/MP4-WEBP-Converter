# main.py

import os
from converter import convert_mp4_to_gif, convert_webp_to_gif
import logging

# Log that the program has started
logging.info("Starting conversion process.")

# Default folders
input_folder = "input_videos"
output_folder = "output_gifs"

# Ensure folders exist
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Get files from input folder
files = os.listdir(input_folder)

# If no files, log and exit
if not files:
    logging.warning("No files found in input folder.")
else:
    for file in files:
        ext = file.lower().split(".")[-1]

        if ext == "mp4":
            convert_mp4_to_gif(file, input_folder, output_folder)
        elif ext == "webp":
            convert_webp_to_gif(file, input_folder, output_folder)
        else:
            logging.info(f"Unsupported file type: {file}")

logging.info("All tasks completed.")
