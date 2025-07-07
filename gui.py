import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging
import time
from tkinter import ttk
from converter import convert_mp4_to_gif, convert_webp_to_gif

# Logging setup
logging.basicConfig(
    filename='conversion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Globals
input_folder = "input_videos"
output_folder = "output_gifs"
filename_prefix = "newgif"
prefix_file = "prefix.txt"
cancel_requested = False

def load_prefix():
    global filename_prefix
    if os.path.exists(prefix_file):
        with open(prefix_file, "r") as f:
            filename_prefix = f.read().strip()

def save_prefix():
    with open(prefix_file, "w") as f:
        f.write(filename_prefix)

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
    global filename_prefix, cancel_requested
    cancel_requested = False
    start_total = time.perf_counter()

    prefix = prefix_entry.get().strip()
    filename_prefix = prefix if prefix else "newgif"
    save_prefix()

    if not os.path.isdir(input_folder):
        messagebox.showerror("Error", "Input folder does not exist.")
        logging.error("Input folder does not exist.")
        return

    os.makedirs(output_folder, exist_ok=True)
    files = os.listdir(input_folder)
    logging.debug(f"Files found in input folder: {files}")

    valid_files = [
        file for file in files
        if os.path.isfile(os.path.join(input_folder, file)) and file.lower().split(".")[-1] in {"mp4", "webp"}
    ]
    total = len(valid_files)

    if not valid_files:
        messagebox.showinfo("No Files", "No MP4 or WEBP files found.")
        logging.warning("No valid files to convert.")
        return

    num_digits = len(str(total))
    durations = []
    count = 1

    progress_bar["maximum"] = total
    progress_bar["value"] = 0

    for file in valid_files:
        if cancel_requested:
            progress_label.config(text="Conversion cancelled.")
            logging.warning("Conversion cancelled by user.")
            return

        ext = file.lower().split(".")[-1]
        input_path = os.path.abspath(os.path.join(input_folder, file))
        output_name = f"{filename_prefix}{str(count).zfill(num_digits)}.gif"
        output_path = os.path.abspath(os.path.join(output_folder, output_name))

        try:
            start_time = time.perf_counter()

            if ext == "mp4":
                convert_mp4_to_gif(input_path, output_path)
            elif ext == "webp":
                convert_webp_to_gif(input_path, output_path)

            elapsed = time.perf_counter() - start_time
            durations.append(elapsed)
            avg_duration = sum(durations) / len(durations)
            remaining = total - count
            eta = round(avg_duration * remaining)

            progress_label.config(
                text=f"Converted {count}/{total} | Last: {elapsed:.2f}s | ETA: {eta}s"
            )
            progress_bar["value"] = count
            window.update_idletasks()
            logging.info(f"Converted {file} to {output_name} in {elapsed:.2f}s")
            count += 1

        except Exception as e:
            logging.error(f"Error converting {file}: {e}")
            progress_label.config(text=f"Error converting {file}")
            window.update_idletasks()

    total_elapsed = time.perf_counter() - start_total
    progress_label.config(text=f"Conversion complete in {round(total_elapsed, 2)} seconds.")
    messagebox.showinfo("Done", f"All files converted.\nTime taken: {round(total_elapsed, 2)} seconds.")
    logging.info(f"Total conversion time: {round(total_elapsed, 2)} seconds")

# GUI setup
window = tk.Tk()
window.title("MP4 & WEBP to GIF Converter")
window.geometry("520x350")
window.resizable(False, False)

# Load prefix
load_prefix()

# Input folder
input_label = tk.Label(window, text=f"Input: {input_folder}")
input_label.pack(pady=5)

input_btn = tk.Button(window, text="Select Input Folder", command=select_input_folder)
input_btn.pack()

# Output folder
output_label = tk.Label(window, text=f"Output: {output_folder}")
output_label.pack(pady=5)

output_btn = tk.Button(window, text="Select Output Folder", command=select_output_folder)
output_btn.pack()

# Prefix field
prefix_frame = tk.Frame(window)
prefix_frame.pack(pady=5)

tk.Label(prefix_frame, text="Filename Prefix:").pack(side=tk.LEFT)
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.insert(0, filename_prefix)
prefix_entry.pack(side=tk.LEFT)

# Progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Progress label
progress_label = tk.Label(window, text="", fg="blue")
progress_label.pack()

# Convert and Cancel buttons
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

convert_btn = tk.Button(btn_frame, text="Convert Files", command=run_conversion, bg="green", fg="white", width=15)
convert_btn.grid(row=0, column=0, padx=10)

cancel_btn = tk.Button(btn_frame, text="Cancel", command=cancel_conversion, bg="red", fg="white", width=15)
cancel_btn.grid(row=0, column=1, padx=10)

# Start GUI
window.mainloop()
