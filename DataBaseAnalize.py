from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def SaveTradeHis():
    user_profile = "C:/Users/Edo/AppData/Local/Google/Chrome/User Data"
    project_folder = os.path.join(os.getcwd(), "SavedTradeHistory")  # Creates a "project_folder" in the current working directory
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_profile}")

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
    time.sleep(3)
    driver.quit()

SaveTradeHis()
