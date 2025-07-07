import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging
from converter import convert_mp4_to_gif, convert_webp_to_gif

# Configure logging
logging.basicConfig(
    filename='conversion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Default folders and prefix
input_folder = "input_videos"
output_folder = "output_gifs"
filename_prefix = "newgif"

def select_input_folder():
    global input_folder
    folder = filedialog.askdirectory()
    if folder:
        input_folder = folder
        input_label.config(text=f"Input: {input_folder}")
        logging.info(f"Selected input folder: {input_folder}")

def select_output_folder():
    global output_folder
    folder = filedialog.askdirectory()
    if folder:
        output_folder = folder
        output_label.config(text=f"Output: {output_folder}")
        logging.info(f"Selected output folder: {output_folder}")

def run_conversion():
    global filename_prefix
    prefix = prefix_entry.get().strip()
    filename_prefix = prefix if prefix else "newgif"

    if not os.path.isdir(input_folder):
        messagebox.showerror("Error", "Input folder does not exist.")
        logging.error("Input folder does not exist.")
        return

    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)
    logging.debug(f"Files found in input folder: {files}")
    print(f"DEBUG: Files in folder: {files}")

    if not files:
        messagebox.showinfo("No Files", "No files found in the input folder.")
        logging.warning("No files found in input folder.")
        return

    gif_index = 1

    for file in files:
        input_path = os.path.abspath(os.path.join(input_folder, file))

        if not os.path.isfile(input_path):
            logging.debug(f"Skipping non-file item: {input_path}")
            print(f"DEBUG: Skipping non-file item: {input_path}")
            continue

        ext = file.lower().split(".")[-1]
        output_name = f"{filename_prefix}{gif_index}.gif"
        output_path = os.path.abspath(os.path.join(output_folder, output_name))

        logging.debug(f"INPUT_PATH: {input_path}")
        logging.debug(f"OUTPUT_PATH: {output_path}")
        print(f"DEBUG: {input_path}")
        print(f"DEBUG: {output_path}")

        try:
            if ext == "mp4":
                convert_mp4_to_gif(input_path, output_path)
                gif_index += 1
            elif ext == "webp":
                convert_webp_to_gif(input_path, output_path)
                gif_index += 1
            else:
                logging.info(f"Unsupported file type: {file}")
                print(f"DEBUG: Unsupported file type: {file}")
        except Exception as e:
            logging.error(f"Error converting {file}: {e}")
            print(f"DEBUG: Error converting {file}: {e}")

    messagebox.showinfo("Done", "All files converted successfully.")
    logging.info("Conversion process completed.")

# Set up GUI window
window = tk.Tk()
window.title("MP4 & WEBP to GIF Converter")
window.geometry("500x300")
window.resizable(False, False)

# Input folder section
input_label = tk.Label(window, text=f"Input: {input_folder}")
input_label.pack(pady=5)

input_btn = tk.Button(window, text="Select Input Folder", command=select_input_folder)
input_btn.pack()

# Output folder section
output_label = tk.Label(window, text=f"Output: {output_folder}")
output_label.pack(pady=5)

output_btn = tk.Button(window, text="Select Output Folder", command=select_output_folder)
output_btn.pack()

# Prefix entry
prefix_frame = tk.Frame(window)
prefix_frame.pack(pady=10)
tk.Label(prefix_frame, text="Output Filename Prefix:").pack(side="left")
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.insert(0, filename_prefix)
prefix_entry.pack(side="left")

# Convert button
convert_btn = tk.Button(window, text="Convert Files", command=run_conversion, bg="green", fg="white")
convert_btn.pack(pady=20)

# Run the GUI event loop
window.mainloop()
