import collectData
import tkinter as tk
from tkinter import filedialog

def save_file(d):
    # Open a file dialog to select a save location
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Check if a save location was selected
    if save_path:
        # Write data to the selected file
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(d)

        print("Data has been saved to:", save_path)
    else:
        print("No save location selected.")

def output(term, num):
    sentences = collectData.data(term,num)

    result = ""
    for values in sentences.values():
        result += values + "\n"

    print(result)

    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Call the save_file function to open the file dialog
    save_file(result)