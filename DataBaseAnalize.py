from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import zipfile
import pandas as pd
import re

def SaveTradeHisPrices():
    user_profile = "C:/Users/Edo/AppData/Local/Google/Chrome/User Data"
    project_folder = os.path.join(os.getcwd(), "SavedTradeHistory")  # Creates a "project_folder" in the current working directory
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_profile}")

    # Set the download directory to the project folder
    prefs = {
        "download.default_directory": project_folder,  # Set the download directory to the project folder
        "download.prompt_for_download": False,  # Disable download prompts
        "directory_upgrade": True  # Automatically download to the specified directory
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver with the options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    url = "https://www.goatbots.com/ajax/trade-history-download"
    driver.get(url)
    time.sleep(3)  # Wait for the download to complete
    url = "https://www.goatbots.com/download/price-history.zip"
    driver.get(url)
    time.sleep(3)  # Wait for the download to complete

    # Quit the driver
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

#import pandas as pd
import re

# Define file paths
collection_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/Full Trade List.csv"
trade_history_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/goatbots-trade-history.csv"
price_history_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/price-history-2024-06-27.txt"

# Load the trade history data
trade_history = pd.read_csv(trade_history_path)

# Load and clean the price history data
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
get_trades.loc[:, 'potential_gain'] = get_trades.apply(
    lambda row: price_data.get(str(row['itemID']), 0) - row['price'],
    axis=1
)

# Sort by potential gain
profitable_trades = get_trades.sort_values(by='potential_gain', ascending=False)

# Load the current collection
collection = pd.read_csv(collection_path)

# Filter the profitable trades to include only cards in the collection
collection_item_ids = collection['ID #'].astype(str).tolist()
collection_names = collection['Card Name'].tolist()
filtered_trades = profitable_trades[profitable_trades['itemID'].astype(str).isin(collection_item_ids)]

# Display the most profitable trades in the collection
for index, row in filtered_trades.head(20).iterrows():
    print(f"Card Name: {row['name']}, Potential Gain: {row['potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}")

# Call the function
#SaveTradeHisPrices()
