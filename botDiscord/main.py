import pyautogui
import time
import random

time.sleep(5)
for i in range(1, 30):
    f = random.choice(list(open("text.txt", "r")))
    pyautogui.typewrite(f)
    pyautogui.press("enter")
    time.sleep(random.randint(70, 140))
