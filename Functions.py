import os
import time
import pyautogui
import pytesseract
from PIL import ImageGrab, Image
import fuzz
from fuzzywuzzy import fuzz
from mss import mss
import subprocess
import pygetwindow as gw
from pywinauto import Application
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import zipfile
from datetime import datetime, timedelta

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract OCR/tesseract.exe"

# Define file paths
collection_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/Full Trade List.csv"
trade_history_path = "C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/goatbots-trade-history.csv"
# Dynamic price history path based on the current date
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
price_history_path = f"C:/Users/edo/PycharmProjects/MTGOautoSeller/SavedTradeHistory/price-history-{yesterday}.txt"
def startmtgoapp():
    if (is_MainNavigation_running()== False):
        os.startfile("C:/Users/edo/Desktop/Magic The Gathering Online .appref-ms")
        time.sleep(5)
        maximize_window("Magic: The Gathering Online")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.typewrite("P_A7uDre")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(30)
    else:
        maximize_window("Magic: The Gathering Online")
def clickonscreen(TargetText, confidence_threshold=50, fuzz_threshold=90):
    screenshot_path = "screenshot.png"
    with mss() as sct:
        sct.shot(output=screenshot_path)

    image = Image.open(screenshot_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    print(data)
    found = False
    TargetText = TargetText.strip()
    target_words = TargetText.split()
    target_length = len(target_words)

    for i in range(len(data['text']) - target_length + 1):
        words = data['text'][i:i + target_length]
        confidences = data['conf'][i:i + target_length]
        ocr_phrase = ' '.join([word.strip() for word in words])

        if all(int(confidences[j]) >= confidence_threshold for j in range(target_length)):
            match_ratio = fuzz.ratio(ocr_phrase, TargetText)
            if match_ratio >= fuzz_threshold:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                center_x, center_y = x + w // 2, y + h // 2
                found = True
                break

    if not found:
        raise ValueError(f"'{TargetText}' not found with sufficient confidence in the screenshot.")

    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()
    os.remove(screenshot_path)
def clickonscreenold(TargetText, confidence_threshold=50):
    screenshot_path = "screenshot.png"
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    image = Image.open(screenshot_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    print(data)
    found = False
    TargetText = TargetText.strip()
    target_words = TargetText.split()
    target_length = len(target_words)

    for i in range(len(data['text']) - target_length + 1):
        # Extract words and confidences for the current slice
        words = data['text'][i:i + target_length]
        confidences = data['conf'][i:i + target_length]
        ocr_phrase = ' '.join([word.strip() for word in words])

        # Check if the OCR phrase matches the target phrase
        if ocr_phrase == TargetText and all(int(confidences[j]) >= confidence_threshold for j in range(target_length)):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            center_x, center_y = x + w // 2, y + h // 2
            found = True
            break

    if not found:
        raise ValueError(f"'{TargetText}' not found with sufficient confidence in the screenshot.")
    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()
    os.remove(screenshot_path)
def clickonscreenrestricted(TargetText, region=(0, 0, 1920, 1080), confidence_threshold=50):
    screenshot_path = "screenshot.png"
    screenshot = ImageGrab.grab(bbox=region)
    screenshot.save(screenshot_path)
    image = Image.open(screenshot_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    found = False
    TargetText = TargetText.strip()
    target_words = TargetText.split()
    target_length = len(target_words)

    for i in range(len(data['text']) - target_length + 1):
        # Extract words and confidences for the current slice
        words = data['text'][i:i + target_length]
        confidences = data['conf'][i:i + target_length]
        ocr_phrase = ' '.join([word.strip() for word in words])

        # Check if the OCR phrase matches the target phrase
        if ocr_phrase == TargetText and all(int(confidences[j]) >= confidence_threshold for j in range(target_length)):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            center_x, center_y = x + w // 2, y + h // 2
            found = True
            break

    if not found:
        raise ValueError(f"'{TargetText}' not found with sufficient confidence in the screenshot.")
        print(data)

    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()
    os.remove(screenshot_path)
def clickonimage(relative_path):
    dirname = os.path.dirname(__file__)
    print(dirname)
    filename = (os.path.join(dirname, relative_path))
    print(filename)
    element = pyautogui.locateOnScreen(filename,confidence=0.7)
    pyautogui.click(element)
def rightclickonimage(relative_path):
    dirname = os.path.dirname(__file__)
    print(dirname)
    filename = (os.path.join(dirname, relative_path))
    print(filename)
    element = pyautogui.locateOnScreen(filename,confidence=0.7)
    pyautogui.rightClick(element)
def checkifimagepresent(relative_path):
    dirname = os.path.dirname(__file__)
    print(dirname)
    filename = os.path.join(dirname, relative_path)
    print(filename)
    try:
        element = pyautogui.locateOnScreen(filename, confidence=0.7)
        if element is not None:
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def AddCardsToOpenBinder(CardName):
    clickonscreen("COLLECTION")
    time.sleep(15)
    clickonimage("Images\Add Binder.png")
    time.sleep(5)
    i = 18
    while i>=0:
        pyautogui.press("Tab")
        i = i-1
        time.sleep(0.1)
    pyautogui.typewrite("BOT BINDER")
    pyautogui.press("enter")
    time.sleep(5)
    clickonscreen("Search for text on cards")
    pyautogui.typewrite(CardName)
    pyautogui.press("enter")
    time.sleep(6)
    pyautogui.moveTo(400, 500)
    pyautogui.rightClick()
    time.sleep(5)
    clickonscreen("Select All")
    time.sleep(5)
    pyautogui.moveTo(400, 150)
    pyautogui.rightClick()
    time.sleep(1)
    clickonscreenold("Add All to Open Binder")
def is_MainNavigation_running():
    try:
        # Run tasklist and check for process name
        output = subprocess.check_output('tasklist', shell=True, text=True)
        if "MTGO.exe" in output:
            print("Main Navigation is running")
            return True
        else:
            print("Main Navigation is not running")
            return False
    except subprocess.CalledProcessError:
        print("Main Navigation is not running")
        return False
def maximize_window(window_title):
    try:
        # Find the window by title
        window = gw.getWindowsWithTitle(window_title)[0]
        # Use pywinauto to maximize the window
        app = Application().connect(handle=window._hWnd)
        app.window(handle=window._hWnd).maximize()
        print(f"Window '{window_title}' has been maximized.")
    except IndexError:
        print(f"No window found with the title '{window_title}'.")
    except Exception as e:
        print(f"Failed to maximize window '{window_title}'. Error: {e}")
def TradeWithGoatbotsSell():
    clickonscreen("TRADE")
    time.sleep(2)
    i = 11
    while i >= 1:
        pyautogui.press("Tab")
        i = i-1
        time.sleep(0.3)
    pyautogui.press("Goatbots")
    pyautogui.press("Enter")
    clickonimage("\Images\Open+Sell.png")
    pyautogui.click()
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
    excluded_file = "Full Trade List.csv"
    for filename in os.listdir(project_folder):
        file_path = os.path.join(project_folder, filename)
        if filename != excluded_file:
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
    trade_history = trade_history[
        ~trade_history['name'].str.contains('booster', case=False) & (trade_history['name'] != 'Event Ticket')]
    with open(price_history_path, 'r') as file:
        lines = file.readlines()
    price_data = {}
    for line in lines:
        cleaned_line = line.replace(',', '').strip()
        match = re.match(r'"(\d+)":\s*(\d+\.\d+)', cleaned_line)
        if match:
            itemID = match.group(1)
            price = float(match.group(2))
            price_data[itemID] = price

    # Convert price data of today to a DataFrame for easier handling
    price_history = pd.DataFrame(list(price_data.items()), columns=['itemID', 'price'])

    # Filter for 'get' trades
    get_trades = trade_history[trade_history['method'] == 'get'].copy()
    # Calculate the potential gain
    get_trades['potential_gain'] = get_trades.apply(lambda row: price_data.get(str(row['itemID']), 0) - row['price'],axis=1)
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
        result += f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Gain: {row['total_potential_gain']}, Unitary Potential Gain: {row['potential_gain']}  Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}\n"

    # Sort by total potential gain in ascending order to find the worst trades
    worst_trades = filtered_trades_with_collection.sort_values(by='total_potential_gain').head(20)

    result += "\nTop 20 Worst Trades:\n"
    for index, row in worst_trades.iterrows():
        result += f"Card Name: {row['Card Name']}, Quantity: {row['Quantity']}, Total Potential Loss: {row['total_potential_gain']}, Price bought: {row['price']}, Price now: {row['price'] + row['potential_gain']}\n"

    return result
def analyze_historic(trade_history_path):
    # Load trade history
    trade_history = pd.read_csv(trade_history_path)

    # Filter out 'Event Ticket' entries and entries containing 'booster'
    trade_history = trade_history[~trade_history['name'].str.contains('booster', case=False) & (trade_history['name'] != 'Event Ticket')]

    # Separate buy and sell transactions
    buy_trades = trade_history[trade_history['method'] == 'get'].copy()
    sell_trades = trade_history[trade_history['method'] == 'give'].copy()

    # Merge buy and sell trades on 'itemID' and 'name' to calculate profit
    merged_trades = pd.merge(buy_trades, sell_trades, on=['name'], suffixes=('_buy', '_sell'))

    # Ensure quantities match for fair profit calculation
    merged_trades['quantity'] = merged_trades[['quantity_buy', 'quantity_sell']].min(axis=1)

    # Calculate profit for each merged trade
    merged_trades['profit'] = (merged_trades['price_sell'] * merged_trades['quantity']) - (merged_trades['price_buy'] * merged_trades['quantity'])

    # Calculate total gain
    total_gain = merged_trades['profit'].sum()

    # Sort trades by profit
    top_30_best_trades = merged_trades.sort_values(by='profit', ascending=False).head(30)
    top_30_worst_trades = merged_trades[merged_trades['profit'] < 0].sort_values(by='profit', ascending=True).head(30)

    # Prepare result string
    result = (
        f"Total Gain from Trades: {total_gain}\n\n"
        "Top 30 Best Trades:\n"
    )

    for index, row in top_30_best_trades.iterrows():
        result += (
            f"Card Name: {row['name']}, Quantity: {row['quantity']}, "
            f"Buy Price: {row['price_buy']}, Sell Price: {row['price_sell']}, "
            f"Profit: {row['profit']}\n"
        )

    result += "\nTop 30 Worst Trades:\n"

    for index, row in top_30_worst_trades.iterrows():
        result += (
            f"Card Name: {row['name']}, Quantity: {row['quantity']}, "
            f"Buy Price: {row['price_buy']}, Sell Price: {row['price_sell']}, "
            f"Profit: {row['profit']}\n"
        )

    return result
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
            "https://www.goatbots.com/download/prices/price-history.zip"
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
def query_card_history(card_name):
    # Load trade history
    trade_history = pd.read_csv(trade_history_path)

    # Filter out 'Event Ticket' entries and entries containing 'booster'
    trade_history = trade_history[
        ~trade_history['name'].str.contains('booster', case=False) & (trade_history['name'] != 'Event Ticket')]

    # Filter for the specific card name with exact match
    card_history = trade_history[trade_history['name'].str.match(f'^{card_name}$', case=False)]

    if card_history.empty:
        return f"No trade history found for card: {card_name}"

    # Sort by timestamp
    card_history = card_history.sort_values(by='timestamp')

    # Create result string
    result = f"Trade History for {card_name}:\n\n"

    total_gain_now = 0  # Initialize total gain now

    for index, row in card_history.iterrows():
        total_tix = row['price'] * row['quantity']
        if row['method'] == 'get':
            result += (
                f"{row['time_cet']}: Bought {row['quantity']} {row['name']} at {row['price']} TIX each, "
                f"For a total of: {total_tix} TIX\n\n"
            )
            total_gain_now -= total_tix  # Subtract buy price
        elif row['method'] == 'give':
            result += (
                f"{row['time_cet']}: Sold {row['quantity']} {row['name']} at {row['price']} TIX each, "
                f"For a total of: {total_tix} TIX\n\n"
            )
            total_gain_now += total_tix  # Add sell price

    # Load collection
    collection = pd.read_csv(collection_path)

    # Filter collection for the specific card name with exact match
    card_collection = collection[collection['Card Name'].str.match(f'^{card_name}$', case=False)]
    total_quantity = card_collection['Quantity'].sum()
    print(f"Total quantity of {card_name} in collection: {total_quantity}")

    # Load price history
    with open(price_history_path, 'r') as file:
        lines = file.readlines()

    price_data = {}
    for line in lines:
        cleaned_line = line.replace(',', '').strip()
        match = re.match(r'"(\d+)":\s*(\d+\.\d+)', cleaned_line)
        if match:
            itemID = match.group(1)
            price = float(match.group(2))
            price_data[itemID] = price

    # Calculate the total value now
    total_value_now = 0
    for index, row in card_collection.iterrows():
        item_id = str(row['ID #'])
        current_price = price_data.get(item_id, 0)
        card_value = row['Quantity'] * current_price
        total_value_now += card_value
        print(
            f"Item ID: {item_id}, Current Price: {current_price}, Quantity: {row['Quantity']}, Card Value: {card_value}")

    print(f"Total value of {card_name} in collection now: {total_value_now} TIX")

    result += f"Total in collection now: {total_quantity}\n"
    result += f"Total value now: {total_value_now} TIX\n"
    result += f"Total gain: {total_gain_now} TIX\n"
    result += f"Total asset value(Tix+value of cards): {total_gain_now+total_value_now} TIX\n"

    return result



