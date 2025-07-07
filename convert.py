# Import necessary libraries
import os
import logging                                 # For file-based logging
from moviepy.editor import VideoFileClip      # For converting MP4 videos to GIFs
from PIL import Image                          # For converting WEBP images to GIFs

# ------------------- LOGGING SETUP -------------------

# Configure logging to write to 'converter.log'
logging.basicConfig(
    filename='converter.log',
    filemode='a',  # Append to existing log
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ------------------- FOLDER SETUP -------------------

# Set names of input and output folders
input_folder = "input_videos"
output_folder = "output_gifs"

# Create the input and output folders if they don't already exist
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# ------------------- CONVERSION FUNCTIONS -------------------

# Function to convert an MP4 video to a GIF
def convert_mp4_to_gif(filename):
    input_path = os.path.join(input_folder, filename)
    output_name = os.path.splitext(filename)[0] + ".gif"
    output_path = os.path.join(output_folder, output_name)

    try:
        print(f"Converting MP4: {filename}")
        logging.info(f"Converting MP4: {filename}")
        clip = VideoFileClip(input_path)
        clip.write_gif(output_path)
        print(f"Saved GIF: {output_name}")
        logging.info(f"Saved GIF: {output_name}")
    except Exception as e:
        print(f"Error converting {filename}: {e}")
        logging.error(f"Error converting {filename}: {e}")

# Function to convert a WEBP image (static or animated) to a GIF
def convert_webp_to_gif(filename):
    input_path = os.path.join(input_folder, filename)
    output_name = os.path.splitext(filename)[0] + ".gif"
    output_path = os.path.join(output_folder, output_name)

    try:
        print(f"Converting WEBP: {filename}")
        logging.info(f"Converting WEBP: {filename}")
        with Image.open(input_path) as im:
            im.save(output_path, format="GIF", save_all=True)
        print(f"Saved GIF: {output_name}")
        logging.info(f"Saved GIF: {output_name}")
    except Exception as e:
        print(f"Error converting {filename}: {e}")
        logging.error(f"Error converting {filename}: {e}")

# ------------------- MAIN LOOP -------------------

files = os.listdir(input_folder)

if not files:
    print("No files found in input folder.")
    logging.info("No files found in input folder.")
else:
    for file in files:
        ext = file.lower().split(".")[-1]
        if ext == "mp4":
            convert_mp4_to_gif(file)
        elif ext == "webp":
            convert_webp_to_gif(file)
        else:
            print(f"Unsupported file type: {file}")
            logging.warning(f"Unsupported file type: {file}")

print("Done.")
logging.info("Conversion process complete.")
