import os
import time
import pyautogui
import pytesseract
from PIL import ImageGrab, Image
import fuzz
from fuzzywuzzy import fuzz
from mss import mss
import subprocess

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract OCR/tesseract.exe"
def startmtgoapp():
    os.startfile("C:/Users/edo/Desktop/Magic The Gathering Online .appref-ms")
    time.sleep(5)
    maximize_MTGO()
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.typewrite("P_A7uDre")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(30)
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
        output = subprocess.check_output(f'tasklist | findstr /I "MainNavigation"', shell=True)
        if "MainNavigation" in str(output):
            return True
    except subprocess.CalledProcessError:
        return False
def TradeWithGoatbotsSell():
    clickonscreen("TRADE")
    time.sleep(1)
    i = 11
    while i >= 1:
        pyautogui.press("Tab")
        i = i-1
        time.sleep(0.1)
    pyautogui.press("Goatbots")
    pyautogui.press("Enter")
    clickonimage("\Images\Open+Sell.png")
    pyautogui.click()
def maximize_MTGO():
    if checkifimagepresent("Images\Maximize.png"):
        clickonimage("Images\Maximize.png")