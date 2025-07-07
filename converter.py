# converter.py

import logging
from moviepy.editor import VideoFileClip
from PIL import Image

def convert_mp4_to_gif(input_path, output_path):
    try:
        logging.info(f"Converting MP4: {input_path}")
        clip = VideoFileClip(input_path)
        clip.write_gif(output_path)
        logging.info(f"Saved GIF: {output_path}")
    except Exception as e:
        logging.error(f"Error converting {input_path}: {e}")


def convert_webp_to_gif(input_path, output_path):
    try:
        logging.info(f"Converting WEBP: {input_path}")
        with Image.open(input_path) as im:
            im.save(output_path, format="GIF", save_all=True)
        logging.info(f"Saved GIF: {output_path}")
    except Exception as e:
        logging.error(f"Error converting {input_path}: {e}")
