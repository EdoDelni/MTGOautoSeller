import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import time
import zipfile
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from Functions import startmtgoapp, clickonscreen, rightclickonimage, clickonimage
import pyautogui

# Define file paths
collection_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/Full Trade List.csv"
trade_history_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/goatbots-trade-history.csv"
# Dynamic price history path based on the current date
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
price_history_path = f"C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/price-history-{yesterday}.txt"


def SaveMtgoCollectionToCSV():
    startmtgoapp()
    clickonscreen("COLLECTION")
    time.sleep(40)
    rightclickonimage("C:/Users/edo/PycharmProjects/MTGOautoSeller/Images/Collection Save.png")
    time.sleep(1)
    pyautogui.leftClick()
    pyautogui.press("Tab")
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("Enter")
    pyautogui.press("Enter")
    pyautogui.press("Enter")

def download_files(user_profile, project_folder):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_profile}")

    # Set the download directory to the project folder
    prefs = {
        "download.default_directory": project_folder,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver with the options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the URL and download files
        urls = [
            "https://www.goatbots.com/ajax/trade-history-download",
            "https://www.goatbots.com/download/price-history.zip"
        ]
        for url in urls:
            driver.get(url)
            time.sleep(3)  # Wait for the download to complete

        # Unzip the downloaded file
        zip_file_path = os.path.join(project_folder, "price-history.zip")
        if os.path.exists(zip_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(project_folder)
    finally:
        # Quit the driver
        driver.quit()


def restore_default_download_settings(user_profile):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_profile}")

    # Reset the preferences
    prefs = {
        "download.default_directory": "",
        "download.prompt_for_download": True,
        "directory_upgrade": False
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver with the options to apply the default settings
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open a blank page to apply the settings
        driver.get("about:blank")
        time.sleep(1)  # Wait for the settings to be applied
    finally:
        # Quit the driver
        driver.quit()


def refresh_database():
    # Clean up the download folder
    project_folder = os.path.join(os.getcwd(), "SavedTradeHistory")
    for filename in os.listdir(project_folder):
        file_path = os.path.join(project_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
    user_profile = "C:/Users/Edo/AppData/Local/Google/Chrome/User Data"
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    try:
        SaveMtgoCollectionToCSV()
        download_files(user_profile, project_folder)
    finally:
        restore_default_download_settings(user_profile)

def refresh_database2():
    # Clean up the download folder
    project_folder = os.path.join(os.getcwd(), "SavedTradeHistory")
    for filename in os.listdir(project_folder):
        file_path = os.path.join(project_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
    user_profile = "C:/Users/Edo/AppData/Local/Google/Chrome/User Data"
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    try:
        #SaveMtgoCollectionToCSV()
        download_files(user_profile, project_folder)
    finally:
        restore_default_download_settings(user_profile)

def analyze_best_and_worst_trades():
    trade_history = pd.read_csv(trade_history_path)
    with open(price_history_path, 'r') as file:
        lines = file.readlines()
    # Remove commas and whitespace, then extract itemID and price using regex
    price_data = {}
    for line in lines:
        cleaned_line = line.replace(',', '').strip()
        match = re.match(r'"(\d+)":\s*(\d+\.\d+)', cleaned_line)
        if match:
            itemID = match.group(1)
            price = float(match.group(2))
            price_data[itemID] = price

    # Convert price data to a DataFrame for easier handling
    price_history = pd.DataFrame(list(price_data.items()), columns=['itemID', 'price'])

    # Filter for 'get' trades
    get_trades = trade_history[trade_history['method'] == 'get'].copy()

    # Calculate the potential gain
    get_trades['potential_gain'] = get_trades.apply(
        lambda row: price_data.get(str(row['itemID']), 0) - row['price'],
        axis=1
    )

    # Sort by potential gain
    profitable_trades = get_trades.sort_values(by='potential_gain', ascending=False)

    # Load the current collection
    collection = pd.read_csv(collection_path)

    # Filter the profitable trades to include only cards in the collection
    collection_item_ids = collection['ID #'].astype(str).tolist()
    filtered_trades = profitable_trades[profitable_trades['itemID'].astype(str).isin(collection_item_ids)]

    # Merge the filtered trades with the collection to get the quantity
    filtered_trades_with_collection = filtered_trades.merge(
        collection[['ID #', 'Card Name', 'Quantity']],
        left_on='itemID',
        right_on='ID #',
        how='left'
    )

    # Calculate total potential gain by multiplying potential gain by quantity
    filtered_trades_with_collection['total_potential_gain'] = filtered_trades_with_collection['potential_gain'] * \
                                                              filtered_trades_with_collection['Quantity']

    result = "Top 20 Profitable Trades:\n"
    for index, row in filtered_trades_with_collection.head(20).iterrows():
        result += f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Gain: {row['total_potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}\n"

    # Sort by total potential gain in ascending order to find the worst trades
    worst_trades = filtered_trades_with_collection.sort_values(by='total_potential_gain').head(20)

    result += "\nTop 20 Worst Trades:\n"
    for index, row in worst_trades.iterrows():
        result += f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Loss: {row['total_potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}\n"

    return result


def analyze_historic(trade_history_path):
    # Load trade history
    trade_history = pd.read_csv(trade_history_path)

    # Ensure that 'quantity' column exists
    if 'quantity' not in trade_history.columns:
        print("Error: 'quantity' column is missing in trade history.")
        return "Error: 'quantity' column is missing in trade history."

    # Separate buy and sell transactions
    buy_trades = trade_history[trade_history['method'] == 'get'].copy()
    sell_trades = trade_history[trade_history['method'] == 'give'].copy()

    # Merge buy and sell trades on 'itemID' and 'name' to calculate profit
    merged_trades = pd.merge(
        buy_trades,
        sell_trades,
        on=['itemID', 'name'],
        suffixes=('_buy', '_sell')
    )

    # Calculate profit for each merged trade
    merged_trades['profit'] = (
            (merged_trades['price_sell'] - merged_trades['price_buy']) * merged_trades['quantity_buy']
    )

    # Calculate total gain
    total_gain = merged_trades['profit'].sum()

    # Sort trades by profit
    top_10_best_trades = merged_trades.sort_values(by='profit', ascending=False).head(10)
    top_10_worst_trades = merged_trades.sort_values(by='profit', ascending=True).head(10)

    # Prepare result string
    result = (
        f"Total Gain from Trades: {total_gain}\n\n"
        "Top 10 Best Trades:\n"
    )

    for index, row in top_10_best_trades.iterrows():
        result += (
            f"Card Name: {row['name']}, Quantity: {row['quantity_buy']}, "
            f"Buy Price: {row['price_buy']}, Sell Price: {row['price_sell']}, "
            f"Profit: {row['profit']}\n"
        )

    result += "\nTop 10 Worst Trades:\n"

    for index, row in top_10_worst_trades.iterrows():
        result += (
            f"Card Name: {row['name']}, Quantity: {row['quantity_buy']}, "
            f"Buy Price: {row['price_buy']}, Sell Price: {row['price_sell']}, "
            f"Profit: {row['profit']}\n"
        )

    return result


def main():
    result = analyze_best_and_worst_trades()
    return result


# GUI setup
def run_analysis():
    result = main()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)


def run_historic_analysis():
    result = analyze_historic(trade_history_path)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)


def run_refresh_database():
    refresh_database()
    messagebox.showinfo("Info", "Database refreshed successfully!")

def run_refresh_database2():
    refresh_database2()
    messagebox.showinfo("Info", "Database refreshed successfully!")

# Dark theme colors
bg_color = "#2e2e2e"
fg_color = "#d3d3d3"
button_bg_color = "#3e3e3e"
button_fg_color = "#d3d3d3"

root = tk.Tk()
root.title("MTGO Auto Seller Analysis")

text_widget_bg_color = "#1e1e1e"
text_widget_fg_color = "#ffffff"

root.configure(bg=bg_color)
frame = tk.Frame(root, bg=bg_color)
frame.pack(pady=20, padx=20)

analyze_button = tk.Button(frame, text="Analyze Best and Worst Trades", command=run_analysis)
analyze_button.pack(pady=5)

historic_button = tk.Button(frame, text="Analyze Historic", command=run_historic_analysis)
historic_button.pack(pady=5)

refresh_button = tk.Button(frame, text="Refresh Database", command=run_refresh_database)
refresh_button.pack(pady=5)

refresh_button = tk.Button(frame, text="Refresh Database excluding MTGO collection", command=run_refresh_database2)
refresh_button.pack(pady=5)

result_text = scrolledtext.ScrolledText(frame, width=200, height=200, bg=text_widget_bg_color, fg=text_widget_fg_color, insertbackground=fg_color)
result_text.pack(pady=10)

root.mainloop()
