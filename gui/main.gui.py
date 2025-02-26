import tkinter as tk
from tkinter import ttk
from backend import generate_tweets  # Import the back-end function

def on_generate():
    # Collect user inputs from the GUI
    destination = dest_input.get()
    num_tweets = int(num_tweets_input.get())
    generation_type = time_or_single_option.get()
    selected_threat_types = [listbox.get(i) for i in listbox.curselection()]

    # Call the back-end function with the collected inputs
    generate_tweets(destination, num_tweets, generation_type, selected_threat_types)

# GUI Setup
root = tk.Tk()
root.title("Data Generator Insider Threats")
root.geometry("530x500")
root.resizable(False, False)

insider_threat_types = ["Malicious", "Medical", "Normal"]

# Title and description labels
ttk.Label(root, text="Tweet Generator", font=("Helvetica", 18, "bold")).grid(row=0, column=0, pady=10, padx=10, sticky="nw")
ttk.Label(root, text="Configure your tweet generation parameters", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="w")

# Destination input field
ttk.Label(root, text="Destination").grid(row=2, column=0, pady=5, padx=10, sticky="w")
dest_input = ttk.Entry(root, width=30)
dest_input.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

# Number of tweets input field
ttk.Label(root, text="Number of Tweets").grid(row=4, column=0, pady=5, padx=10, sticky="w")
num_tweets_input = ttk.Entry(root, width=30)
num_tweets_input.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

# Generation Type Radio Buttons
time_or_single_option = tk.StringVar()
time_or_single_option.set("Single")

ttk.Label(root, text="Generation Type").grid(row=6, column=0, pady=5, padx=10, sticky="w")
radio1 = ttk.Radiobutton(root, text="Single Tweet", variable=time_or_single_option, value="Single").grid(row=7, column=0, pady=5, padx=10, sticky="w")
radio2 = ttk.Radiobutton(root, text="Time Series Tweet", variable=time_or_single_option, value="Time Series").grid(row=7, column=0, pady=5, padx=125, sticky="w")

# Insider Threat Types Listbox
ttk.Label(root, text="Insider Threat Types").grid(row=8, column=0, pady=5, padx=10, sticky="w")
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=3, width=30)
for idx, element in enumerate(insider_threat_types):
    listbox.insert(idx, element)
listbox.grid(row=9, column=0, padx=10, pady=5, sticky="w")

# Generate Button
button = ttk.Button(root, text="Generate", width=82, command=on_generate)
button.grid(row=10, column=0, padx=10, pady=10, sticky="w")

root.mainloop()