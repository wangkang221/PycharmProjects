import time
import pyautogui

x,y=pyautogui.position()
print(x,y)
# 飞书 54 1679
# IPOS 423 756,1939 906,2675 298,3056 616,3063 279
# SOKIT 430 991
# PYCHAR 597 74
pyautogui.doubleClick(423,756)
time.sleep(4)
pyautogui.press('enter')
pyautogui.click(2675,298)
pyautogui.click(3056,616)
pyautogui.click(3063,279)



#pyautogui.moveTo(1801,1154,3)



#pyautogui.moveTo(423,756,1)
