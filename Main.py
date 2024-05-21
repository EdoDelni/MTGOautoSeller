import os
import time
import pyautogui
import pytesseract
from PIL import ImageGrab, Image
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract OCR/tesseract.exe"
def startmtgoapp():
    os.startfile("C:/Users/edo/Desktop/Magic The Gathering Online .appref-ms")
    time.sleep(3)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.typewrite("P_A7uDre")
    pyautogui.press("enter")
    time.sleep(15)


def clickonscreen(TargetText, confidence_threshold=50):
    screenshot_path = "screenshot.png"
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    image = Image.open(screenshot_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    found = False
    print(data['text'])
    # Concatenate the target words to search for the full phrase
    target_phrase = TargetText.lower().split()  # Split the target text into individual words
    target_phrase_length = len(target_phrase)
    for i in range(len(data['text']) - target_phrase_length + 1):
        if ' '.join(data['text'][i:i + target_phrase_length]).lower() == TargetText.lower() \
                and all(int(data['conf'][j]) >= confidence_threshold for j in range(i, i + target_phrase_length)):
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
    screenshot = ImageGrab.grab(bbox=region)  # Capture screenshot of specified region
    screenshot.save(screenshot_path)
    image = Image.open(screenshot_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    found = False
    target_phrase = TargetText.lower().split()
    target_phrase_length = len(target_phrase)
    for i in range(len(data['text']) - target_phrase_length + 1):
        if ' '.join(data['text'][i:i + target_phrase_length]).lower() == TargetText.lower() \
                and all(int(data['conf'][j]) >= confidence_threshold for j in range(i, i + target_phrase_length)):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            center_x, center_y = x + w // 2, y + h // 2
            found = True
            break

    if not found:
        raise ValueError(f"'{TargetText}' not found with sufficient confidence in the specified region.")
    pyautogui.moveTo(region[0] + center_x, region[1] + center_y)  # Adjust to absolute screen coordinates
    pyautogui.click()
    os.remove(screenshot_path)


def clickonimage(relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, relative_path)
    element = pyautogui.locateOnScreen(image_path)
    pyautogui.click(element)

CardName = "Force Of Will"

startmtgoapp()
clickonscreen("Collection")
time.sleep(2)
clickonimage("\Images\Add Binder.png")
time.sleep(2)
pyautogui.press("enter")
clickonscreen("Search for text on cards")
pyautogui.typewrite(CardName)
clickonscreenrestricted(CardName, (300, 0, 1980, 1080))
pyautogui.rightClick()
time.sleep(1)
clickonscreen("Add All to Open Binder")



