import tkinter as tk
import os, sys
from tkinter import ttk, filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend import generate_tweets, generate_timeseries_tweets  # Import the back-end function

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")])
    if filename:
        dest_input.delete(0, tk.END) 
        dest_input.insert(0, filename) 


def check_all_inputs():
    if dest_input.get().strip() == "" or num_tweets_input.get().strip() == "" or time_or_single_option.get() == "" or not listbox.curselection():
        button.config(state=tk.DISABLED)
        return
    
    button.config(state=tk.NORMAL)

def on_listbox_select(event):
    check_all_inputs()
        

def on_generate():
    # Collect user inputs from the GUI
    print("Generating Tweets")
    destination = dest_input.get()
    num_tweets = int(num_tweets_input.get())
    generation_type = time_or_single_option.get()
    selected_threat_types = [listbox.get(i) for i in listbox.curselection()]

    

    # Call the back-end function with the collected inputs
    if(generation_type == "Single"):
        res = generate_tweets(destination, num_tweets, selected_threat_types)  
    else:
        res = generate_timeseries_tweets(destination, num_tweets, selected_threat_types)
    
    print("Done generating")
    button.config(state="normal", text="Generate")

def handle_generate():
    button.config(state=tk.DISABLED, text="Generating Tweets...")
    root.after(100, on_generate)


# GUI Setup
root = tk.Tk()
root.title("Data Generator Insider Threats")
root.geometry("600x500")
#root.resizable(False, False)

insider_threat_types = ["Malicious", "Medical", "Normal"]

# Title and description labels
ttk.Label(root, text="Tweet Generator", font=("Helvetica", 18, "bold")).grid(row=0, column=0, pady=10, padx=10, sticky="nw")
ttk.Label(root, text="Configure your tweet generation parameters", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="w")

# Destination input field
ttk.Label(root, text="Destination").grid(row=2, column=0, pady=5, padx=10, sticky="w")
dest_input = tk.Entry(root)
dest_input.grid(row=3, column=0, pady=5, padx=10, sticky="we")
dest_input.bind("<KeyRelease>", lambda e: check_all_inputs())

browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=3, column=1)

# Number of tweets input field
ttk.Label(root, text="Number of Tweets").grid(row=4, column=0, pady=5, padx=10, sticky="w")
num_tweets_input = ttk.Entry(root, width=30)
num_tweets_input.grid(row=5, column=0, pady=5, padx=10, sticky="ew")
num_tweets_input.bind("<KeyRelease>", lambda e: check_all_inputs())

# Generation Type Radio Buttons
time_or_single_option = tk.StringVar()
time_or_single_option.set("Single")


ttk.Label(root, text="Generation Type").grid(row=6, column=0, pady=5, padx=10, sticky="w")
radio1 = ttk.Radiobutton(root, text="Single Tweet", variable=time_or_single_option, value="Single", command=check_all_inputs).grid(row=7, column=0, pady=5, padx=10, sticky="w")
radio2 = ttk.Radiobutton(root, text="Time Series Tweet", variable=time_or_single_option, value="Time Series", command=check_all_inputs).grid(row=7, column=0, pady=5, padx=125, sticky="w")

# Insider Threat Types Listbox
ttk.Label(root, text="Insider Threat Types").grid(row=8, column=0, pady=5, padx=10, sticky="w")
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=3, width=30)
for idx, element in enumerate(insider_threat_types):
    listbox.insert(idx, element)
listbox.grid(row=9, column=0, padx=10, pady=5, sticky="w")
listbox.bind("<<ListboxSelect>>", on_listbox_select)

# Generate Button
button = ttk.Button(root, text="Generate", width=82, state=tk.DISABLED, command=handle_generate)
button.grid(row=10, column=0, padx=10, pady=10, sticky="w")

root.mainloop()