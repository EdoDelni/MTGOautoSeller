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
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(15)


def clickonscreen(TargetText, confidence_threshold=50):
    screenshot_path = "screenshot.png"
    screenshot = ImageGrab.grab()
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

CardName = "Force Of Will"

startmtgoapp()
clickonscreen("COLLECTION")
time.sleep(10)
clickonimage("Images\Add Binder.png")
time.sleep(2)
pyautogui.press("enter")
time.sleep(2)
clickonscreen("Search for text on cards")
pyautogui.typewrite(CardName)
pyautogui.press("enter")
time.sleep(3)
clickonscreenrestricted(CardName, (300, 0, 1980, 1080))
pyautogui.rightClick()
time.sleep(1)
clickonscreen("Add All to Open Binder")



