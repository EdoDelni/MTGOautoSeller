import tkinter as tk
from tkinter import messagebox, scrolledtext
from Functions import startmtgoapp, clickonscreen, rightclickonimage, clickonimage, SaveMtgoCollectionToCSV, download_files, analyze_historic, analyze_best_and_worst_trades, refresh_database, refresh_database2, query_card_history

# GUI setup
def run_analysis():
    result = analyze_best_and_worst_trades()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

def run_historic_analysis():
    result = analyze_historic()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

def run_refresh_database():
    refresh_database()
    messagebox.showinfo("Info", "Database refreshed successfully!")

def run_refresh_database2():
    refresh_database2()
    messagebox.showinfo("Info", "Database refreshed successfully!")

def query_database():
    card_name = card_name_entry.get()
    result = query_card_history(card_name)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)


bg_color = "#2e2e2e"
fg_color = "#d3d3d3"
button_bg_color = "#3e3e3e"
button_fg_color = "#d3d3d3"
text_widget_bg_color = "#1e1e1e"
text_widget_fg_color = "#ffffff"

# Main window setup
root = tk.Tk()
root.title("MTGO Auto Seller Analysis")
root.configure(bg=bg_color)

# Set the window to be maximized
root.state('zoomed')

# Frame setup
frame = tk.Frame(root, bg=bg_color)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Buttons setup
analyze_button = tk.Button(frame, text="Analyze Best and Worst Trades", command=run_analysis, bg=button_bg_color, fg=button_fg_color)
analyze_button.pack(pady=5)

historic_button = tk.Button(frame, text="Analyze Historic", command=run_historic_analysis, bg=button_bg_color, fg=button_fg_color)
historic_button.pack(pady=5)

refresh_button = tk.Button(frame, text="Refresh Database", command=run_refresh_database, bg=button_bg_color, fg=button_fg_color)
refresh_button.pack(pady=5)

refresh_button2 = tk.Button(frame, text="Refresh Database excluding MTGO collection", command=run_refresh_database2, bg=button_bg_color, fg=button_fg_color)
refresh_button2.pack(pady=5)

# Entry and button for querying the database
card_name_label = tk.Label(frame, text="Enter Card Name:", bg=bg_color, fg=fg_color)
card_name_label.pack(pady=5)

card_name_entry = tk.Entry(frame, bg=text_widget_bg_color, fg=text_widget_fg_color)
card_name_entry.pack(pady=5)

query_button = tk.Button(frame, text="Query Database to search for a card", command=query_database, bg=button_bg_color, fg=button_fg_color)
query_button.pack(pady=5)

# Text widget setup
result_text = scrolledtext.ScrolledText(frame, bg=text_widget_bg_color, fg=text_widget_fg_color, insertbackground=fg_color)
result_text.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()