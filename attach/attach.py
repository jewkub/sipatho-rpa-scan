#!/usr/bin/env python3
import shutil
import time
from pathlib import Path
import tkinter
from tkinter import messagebox
import pyautogui
import re

def withsleep (fn, sleeptime=1.0):
  time.sleep(sleeptime)

if __name__ == "__main__":
  root = tkinter.Tk()
  root.withdraw() # use to hide tkinter window
  messagebox.showinfo("Ready", "หลังจากกด OK แล้วกดไปที่ HCLAB และกดคลิกช่องใส่ Surgical No. ทันที")
  time.sleep(10)

  p = (Path(__file__).parent / 'renamed').glob('*')
  files = [x for x in p if x.is_file()]
  # print(files)
  for file in files:
    # print(re.split('-| ', file.stem)[0].split(','))
    for surgicalNo in re.split('-| ', file.stem)[0].split(','):
      print(surgicalNo)
      surgicalNo = surgicalNo.strip()
      withsleep(pyautogui.write(surgicalNo), 0.2)
      withsleep(pyautogui.press('enter'))
      withsleep(pyautogui.hotkey('ctrl', 'pagedown'), 0.2)
      withsleep(pyautogui.press('enter'))
      withsleep(pyautogui.write(file.stem), 0.6)
      withsleep(pyautogui.press('down'), 0.6)
      withsleep(pyautogui.press('enter'), 2.0)
      withsleep(pyautogui.hotkey('ctrl', 'pagedown'), 0.2)
      withsleep(pyautogui.press('tab', presses=3), 0.2)
      withsleep(pyautogui.press('enter'))
    shutil.move(file, Path(__file__).parent / 'done' / file.name)

# retry = True
# while retry:
#   time.sleep(3)
#   try:
#     x, y = pyautogui.locateCenterOnScreen('testimg.png') # type: ignore
#     pyautogui.click(x, y)
#     pyautogui.write(file.stem)
#     break
#   except pyautogui.ImageNotFoundException:
#     retry = messagebox.askretrycancel("askretrycancel", "Text box not found. Try again?")
