import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging
import time
import shutil
from tkinter import ttk
from converter import convert_video_to_gif, convert_webp_to_gif

# Logging setup
logging.basicConfig(
    filename='conversion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Globals
input_folder = "input_videos"
output_folder = "output"
gif_prefix = "newgif"
image_prefix = "newimage"
prefix_file = "prefix.txt"
cancel_requested = False

def load_prefix():
    global gif_prefix
    if os.path.exists(prefix_file):
        with open(prefix_file, "r") as f:
            gif_prefix = f.read().strip()

def save_prefix():
    with open(prefix_file, "w") as f:
        f.write(gif_prefix)

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

def cancel_conversion():
    global cancel_requested
    cancel_requested = True
    progress_label.config(text="Cancelling...")

def run_conversion():
    global gif_prefix, cancel_requested
    cancel_requested = False
    start_total = time.perf_counter()

    prefix = prefix_entry.get().strip()
    gif_prefix = prefix if prefix else "newgif"
    save_prefix()

    if not os.path.isdir(input_folder):
        messagebox.showerror("Error", "Input folder does not exist.")
        logging.error("Input folder does not exist.")
        return

    gif_output = os.path.join(output_folder, "output_gifs")
    img_output = os.path.join(output_folder, "output_images")
    os.makedirs(gif_output, exist_ok=True)
    os.makedirs(img_output, exist_ok=True)

    supported_video_exts = {"mp4", "webm", "mov"}
    supported_image_exts = {"jpg", "jpeg", "png"}
    gif_count = image_count = 1
    gif_durations = []

    file_list = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_list.append(os.path.join(root, file))

    progress_bar["maximum"] = len(file_list)
    progress_bar["value"] = 0
    progress_label.config(text=f"Found {len(file_list)} total files.")

    for i, file_path in enumerate(file_list):
        if cancel_requested:
            progress_label.config(text="Conversion cancelled.")
            logging.warning("Conversion cancelled by user.")
            return

        ext = file_path.lower().split(".")[-1]
        try:
            start_time = time.perf_counter()

            if ext in supported_video_exts:
                output_name = f"{gif_prefix}{str(gif_count).zfill(4)}.gif"
                output_path = os.path.join(gif_output, output_name)
                convert_video_to_gif(file_path, output_path)
                gif_count += 1

            elif ext == "webp":
                output_name = f"{gif_prefix}{str(gif_count).zfill(4)}.gif"
                output_path = os.path.join(gif_output, output_name)
                convert_webp_to_gif(file_path, output_path)
                gif_count += 1

            elif ext in supported_image_exts:
                output_name = f"{image_prefix}{str(image_count).zfill(4)}.{ext}"
                output_path = os.path.join(img_output, output_name)
                shutil.copy2(file_path, output_path)
                image_count += 1

            elapsed = time.perf_counter() - start_time
            gif_durations.append(elapsed)
            avg_duration = sum(gif_durations) / len(gif_durations) if gif_durations else 0
            eta = round(avg_duration * (len(file_list) - i - 1))

            progress_label.config(
                text=f"Processed {i+1}/{len(file_list)} | ETA: {eta}s"
            )
            progress_bar["value"] = i + 1
            window.update_idletasks()
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            progress_label.config(text=f"Error: {os.path.basename(file_path)}")
            window.update_idletasks()

    total_elapsed = time.perf_counter() - start_total
    progress_label.config(text=f"Complete in {round(total_elapsed, 2)} seconds.")
    messagebox.showinfo("Done", f"Conversion done.\nTime taken: {round(total_elapsed, 2)} seconds.")
    logging.info(f"Finished conversion in {round(total_elapsed, 2)} seconds")

# GUI setup
window = tk.Tk()
window.title("Media File Processor")
window.geometry("520x360")
window.resizable(False, False)

load_prefix()

input_label = tk.Label(window, text=f"Input: {input_folder}")
input_label.pack(pady=5)
tk.Button(window, text="Select Input Folder", command=select_input_folder).pack()

output_label = tk.Label(window, text=f"Output: {output_folder}")
output_label.pack(pady=5)
tk.Button(window, text="Select Output Folder", command=select_output_folder).pack()

prefix_frame = tk.Frame(window)
prefix_frame.pack(pady=5)
tk.Label(prefix_frame, text="GIF Filename Prefix:").pack(side=tk.LEFT)
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.insert(0, gif_prefix)
prefix_entry.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

progress_label = tk.Label(window, text="", fg="blue")
progress_label.pack()

btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Convert Files", command=run_conversion, bg="green", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Cancel", command=cancel_conversion, bg="red", fg="white", width=15).grid(row=0, column=1, padx=10)

def launch_gui():
    window.mainloop()

if __name__ == "__main__":
    launch_gui()
