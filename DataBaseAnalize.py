import os
import time
import zipfile
import pandas as pd
import re
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from Functions import startmtgoapp, clickonscreen, rightclickonimage

# Define file paths
collection_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/Full Trade List.csv"
trade_history_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/goatbots-trade-history.csv"
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
price_history_path = f"C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/price-history-{yesterday}.txt"

def SaveMtgoCollectionToCSV():
    startmtgoapp()
    clickonscreen("COLLECTION")
    time.sleep(15)
    rightclickonimage("C:/Users/edo/PycharmProjects/MTGOautoSeller/Images/Collection Save.png")
    time.sleep(5)
    clickonscreen("Export")
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)
def SaveTradeHisPrices():
    user_profile = "C:/Users/Edo/AppData/Local/Google/Chrome/User Data"
    project_folder = os.path.join(os.getcwd(), "SavedTradeHistory")  # Creates a "project_folder" in the current working directory
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_profile}")
    prefs = {
        "download.default_directory": project_folder,  # Set the download directory to the project folder
        "download.prompt_for_download": False,  # Disable download prompts
        "directory_upgrade": True  # Automatically download to the specified directory
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.goatbots.com/ajax/trade-history-download"
    driver.get(url)
    time.sleep(3)  # Wait for the download to complete
    url = "https://www.goatbots.com/download/price-history.zip"
    driver.get(url)
    time.sleep(3)  # Wait for the download to complete
    driver.quit()

    # Unzip the downloaded file
    zip_file_path = os.path.join(project_folder, "price-history.zip")
    if os.path.exists(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(project_folder)

    # Restore default download settings
    restore_default_download_settings(user_profile)
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

    # Open a blank page to apply the settings
    driver.get("about:blank")
    time.sleep(1)  # Wait for the settings to be applied

    # Quit the driver
    driver.quit()
def AnalizeHistoric():
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
    filtered_trades_with_collection['total_potential_gain'] = filtered_trades_with_collection['potential_gain'] * filtered_trades_with_collection['Quantity']

    # Display the most profitable trades in the collection
    print("Top 20 Profitable Trades:")
    for index, row in filtered_trades_with_collection.head(20).iterrows():
        print(f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Gain: {row['total_potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}")

    # Sort by total potential gain in ascending order to find the worst trades
    worst_trades = filtered_trades_with_collection.sort_values(by='total_potential_gain').head(20)

    # Display the worst trades in the collection
    print("\nTop 20 Worst Trades:")
    for index, row in worst_trades.iterrows():
        print(f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Loss: {row['total_potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}")

        # Function to calculate profit from buy and P_A7uDre
def main():
    print("Saving trade history prices...")
    SaveTradeHisPrices()
    print("Trade history prices saved.\n")

    print("Select a function to execute:")
    print("1. Analyze Trades historic")
    print("2. Analyze Possible trades")

    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        AnalizeHistoric()
    elif choice == '2':
        trade_history = pd.read_csv(trade_history_path)

    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
