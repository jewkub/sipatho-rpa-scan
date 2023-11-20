#!/usr/bin/env python3
import sys
import shutil
import os
from pyzbar import pyzbar
from pathlib import Path
import cv2
import tkinter
from tkinter import filedialog
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_path(prompt):
  tempdir = filedialog.askdirectory(
    parent=root,
    initialdir=Path.cwd(),
    title='Select a directory for ' + prompt + ' files',
  )
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

  return (image, decoded_objects)

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

class ScannedFileHandler(FileSystemEventHandler):
  def on_created(self, event):
    # dir_path = event.src_path.split('/input_files')
    # processed_files = f'{dir_path[0]}/processed_files'
    # child_processed_dir = create_directory(file_path=processed_files)
    if event:
      objs = None
      print("file created:{}".format(event.src_path))
      if not event.src_path:
        print("Invalid file path")
        return
      file_path = Path(event.src_path).as_posix()
      old_size = -1
      while (old_size != os.path.getsize(file_path)):
        old_size = os.path.getsize(file_path)
        time.sleep(0.1)
      img = cv2.imread(file_path)
      (img, objs) = decode(img)
      # cv2.imshow("img", img)
      # cv2.waitKey(0)

      if type(objs) is list and objs[0] is not None:
        file_name = objs[0].data.decode("utf-8") + Path(file_path).suffix
        dest_path = Path(renamed_path) / file_name
        # print(dest_path)
        shutil.move(file_path, dest_path)
        print("file moved:{} to {}".format(file_path, dest_path))
        cv2.destroyAllWindows()

if __name__ == "__main__":
  # print(Path.cwd())
  # DIRNAME = Path(__file__).parent.resolve()
  # print(DIRNAME.as_posix())
  root = tkinter.Tk()
  root.withdraw() # use to hide tkinter window

  scanned_path = get_path('scanned')
  if len(scanned_path) == 0:
    sys.exit(0)
  renamed_path = get_path('renamed')
  if len(renamed_path) == 0:
    sys.exit(0)

  logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
  observer = Observer()
  observer.schedule(ScannedFileHandler(), scanned_path, recursive=True)
  observer.start()

  try:
    while True:
      time.sleep(1000)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
