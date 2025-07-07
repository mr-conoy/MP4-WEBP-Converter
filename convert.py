# Import necessary libraries
import os                                # For file and folder operations
from moviepy.editor import VideoFileClip # For converting MP4 videos to GIFs
from PIL import Image                    # For converting WEBP images to GIFs

# Set names of input and output folders
input_folder = "input_videos"
output_folder = "output_gifs"

# Create the input and output folders if they don't already exist
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Function to convert an MP4 video to a GIF
def convert_mp4_to_gif(filename):
    # Build full input and output file paths
    input_path = os.path.join(input_folder, filename)
    output_name = os.path.splitext(filename)[0] + ".gif"  # Change extension to .gif
    output_path = os.path.join(output_folder, output_name)

    try:
        print(f"Converting MP4: {filename}")
        clip = VideoFileClip(input_path)           # Load the MP4 video
        clip.write_gif(output_path)                # Export it as a GIF
        print(f"Saved GIF: {output_name}")
    except Exception as e:
        print(f"Error converting {filename}: {e}") # Print any errors

# Function to convert a WEBP image (static or animated) to a GIF
def convert_webp_to_gif(filename):
    # Build full input and output file paths
    input_path = os.path.join(input_folder, filename)
    output_name = os.path.splitext(filename)[0] + ".gif"  # Change extension to .gif
    output_path = os.path.join(output_folder, output_name)

    try:
        print(f"Converting WEBP: {filename}")
        with Image.open(input_path) as im:               # Open the WEBP file
            im.save(output_path, format="GIF", save_all=True)  # Save as GIF (supports animation)
        print(f"Saved GIF: {output_name}")
    except Exception as e:
        print(f"Error converting {filename}: {e}")       # Print any errors

# ------------------- MAIN LOOP -------------------

# Get list of all files in the input folder
files = os.listdir(input_folder)

# If the folder is empty, show a message
if not files:
    print("No files found in input folder.")
else:
    # Loop through each file in the folder
    for file in files:
        ext = file.lower().split(".")[-1]  # Get the file extension

        # Use the correct converter based on file type
        if ext == "mp4":
            convert_mp4_to_gif(file)
        elif ext == "webp":
            convert_webp_to_gif(file)
        else:
            print(f"Unsupported file type: {file}")  # Skip unsupported files

print("Done.")
