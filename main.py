import sys
from pyzbar import pyzbar
from pathlib import Path
import cv2
import tkinter
from tkinter import filedialog

# https://stackoverflow.com/a/43046744
# from ctypes import windll
# windll.shcore.SetProcessDpiAwareness(1)

root = tkinter.Tk()
root.withdraw() # use to hide tkinter window

def get_path():
  currdir = Path.cwd()
  tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
  if len(tempdir) > 0:
    print ("You chose: %s" % tempdir)
  return tempdir

def decode(image):
  # decodes all barcodes from an image
  decoded_objects = pyzbar.decode(image)
  for obj in decoded_objects:
    # draw the barcode
    print("detected barcode:", obj)
    image = draw_barcode(obj, image)
    # print barcode type & data
    print("Type:", obj.type)
    print("Data:", obj.data)
    print()

  return image

def draw_barcode(decoded, image):
  # n_points = len(decoded.polygon)
  # for i in range(n_points):
  #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
  # uncomment above and comment below if you want to draw a polygon and not a rectangle
  image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
    (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
    color=(0, 255, 0),
    thickness=5)
  return image

if __name__ == "__main__":
  print(sys.executable)
  DIRNAME = Path(__file__).parent.resolve()
  print(DIRNAME.as_posix())
  path = get_path()
  if len(path) == 0:
    exit()
  barcodes = DIRNAME.glob("barcode*.png")
  for barcode_file in barcodes:
    # load the image to opencv
    print(barcode_file.as_posix())
    img = cv2.imread(barcode_file.as_posix())
    # decode detected barcodes & get the image
    # that is drawn
    img = decode(img)
    # show the image
    cv2.imshow("img", img)
    cv2.waitKey(0)
