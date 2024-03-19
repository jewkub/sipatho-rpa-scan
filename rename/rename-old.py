# %%
import pdf2image
import os
from pdf2image import convert_from_path
from PIL import Image
import glob
import os, sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import easyocr
import re
import shutil

# %%
path_img = f"{os.path.dirname(sys.executable)}\\image"
pdf_origin_path = f"{os.path.dirname(sys.executable)}\\raw"
path_renamed = f"{os.path.dirname(sys.executable)}\\renamed"
reader = easyocr.Reader(['en'])

# %%
def copy_and_rename(src_path, dest_path, new_name):
  new_path = f"{dest_path}\\{new_name}"
  # Copy the file
  # shutil.copy(src_path, new_path)

  # Rename the copied file
  print(f"{src_path}")
  #shutil.move(f"{src_path}", new_path)
  shutil.copy(src_path, new_path)

def read_pdf(file_name):
  try:
    # Convert the PDF file to a list of PIL images:
    images = convert_from_path(file_name, poppler_path=r"C:\Users\jewna\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin")
    # Extract text from each image:
    for i, image in enumerate(images):
      # Generating filename for each image
      filename = path_img+r"\page_" + str(i) + "_" + os.path.basename(file_name) + ".jpeg" 
      # print(filename)
      image.save(filename, "JPEG")  
      break

  except Exception as e:
    print(str(e))

  img = cv2.imread(filename)
  # print(img.shape) # Print image shape
  # cv2.imshow("original", img)
  
  # Cropping an image
  cropped_image = img[0:300, 1100:1659]

  # Display cropped image
  # cv2.imshow("cropped", cropped_image)
  plt.imshow(cropped_image)
  plt.show()

  # Save the cropped image
  cv2.imwrite("Cropped_Image.jpg", cropped_image)

  # Open an image file
  ocr = reader.readtext('Cropped_Image.jpg')
  found = False

  for detection in ocr:
    matched = re.search("[A-Z]{1,3}[0-9]{8}", detection[1])
    if matched:
      new_name = matched.group(0)
      copy_and_rename(file_name, path_renamed, new_name + ".pdf")
      found = True

  if not found:
    rotated_image = cv2.rotate(cropped_image, cv2.ROTATE_180)
    cv2.imwrite("Rotated_Image.jpg", rotated_image)
    ocr = reader.readtext("Rotated_Image.jpg")

    for detection in ocr:
      matched = re.search("[A-Z]{1,3}[0-9]{8}", detection[1])
      if matched:
        new_name = matched.group(0)
        copy_and_rename(file_name, path_renamed, new_name + ".pdf")
        found = True

  if not found:
    print(f"Not Found: {pdf_name}")
    return "failed"

  return "done"
    
# %%
if __name__ == "__main__":
  # print(path_img)
  # print(pdf_origin_path)
  # print(path_renamed)
  for pdf_name in glob.glob(pdf_origin_path + r"\*.pdf"):
    print(read_pdf(pdf_name))