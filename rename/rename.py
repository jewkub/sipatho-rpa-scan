import pdf2image
import os, time
from datetime import datetime
from pdf2image import convert_from_path
# import pytesseract as tess
# Importing the Image module from the PIL package to work with images
from PIL import Image
import pandas as pd
import glob
import cv2, sys
import numpy as np
from matplotlib import pyplot as plt
import easyocr
import re
import shutil

start = time.time()

path_img = f"{os.path.dirname(sys.executable)}\\image"
pdf_origin_path = f"{os.path.dirname(sys.executable)}\\raw"
path_renamed = f"{os.path.dirname(sys.executable)}\\renamed"
reader = easyocr.Reader(['en'])
crop_name = "image.png"

def copy_and_rename(src_path, dest_path, new_name):
  new_path = f"{dest_path}\\{new_name}"
  # Copy the file
  # shutil.copy(src_path, new_path)
  #shutil.move(f"{src_path}", new_path)
  shutil.move(src_path, new_path)

def readOCR(reader, file_name, image_name):
  # Open an image file
  result = reader.readtext(image_name)
  # filter_first = filter(lambda x: re.search("[A-Z]{1,3}[0-9]{8}", x[1]), result_cropped)
  # if len(list(filter_first))==0:
  #   result_rotated = reader.readtext('Cropped_Rotated_Image.jpg')
  #   result = result_rotated
  # else:
  #   result = result_cropped
  found = False
  for detection in result:
    match = re.search("[A-Z]{1,3}[0-9]{8}", detection[1])
    if match:
      # found = True
      new_name = match.group(0)
      # print(detection[1])
      #print(path_renamed, new_name)
      copy_and_rename(file_name, path_renamed, new_name+".pdf")
      # 
      found = True

  if found:
    return True, new_name
  else:
    return False, file_name

def read_pdf(file_name, reader):
  # Store all pages of one file here:
  pages = []

  if os.path.exists("renamed_file.csv"):
    renamed_df = pd.read_csv("renamed_file.csv")
  else:
    renamed_df = pd.DataFrame(columns=["file_name", "sending_status", "timestamp"])

  if os.path.exists("reject_file.csv"):
    reject_df = pd.read_csv("reject_file.csv")
  else:
    reject_df = pd.DataFrame(columns=["file_name", "timestamp"])

  #################################################

  try:
    # Convert the PDF file to a list of PIL images:
    images = convert_from_path(file_name, poppler_path=f"{os.path.dirname(sys.executable)}\\poppler\\Library\\bin")
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
  # Save the cropped image
  cv2.imwrite(crop_name, cropped_image)
  found = False
  found, name = readOCR(reader=reader, file_name=file_name, image_name=crop_name)
  if found:
    print(f"{file_name} Found")
    renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
    renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
  else:
    image_rotated = cv2.rotate(cropped_image, cv2.ROTATE_180)
    cv2.imwrite(crop_name, image_rotated)
    found, name = readOCR(reader=reader, file_name=file_name, image_name=crop_name)
    if found:
      print(f"{file_name} Found")
      renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
      renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
    else:
      cropped_rotated_image = img[2000:2346, 0:600]
      cv2.imwrite(crop_name, image_rotated)
      found, name = readOCR(reader=reader, file_name=file_name, image_name=crop_name)
      if found:
        print(f"{file_name} Found")
        renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
        renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
      else:
        image_rotated = cv2.rotate(cropped_rotated_image, cv2.ROTATE_180)
        cv2.imwrite(crop_name, image_rotated)
        found, name = readOCR(reader=reader, file_name=file_name, image_name=crop_name)
        if found:
          print(f"{file_name} Found")
          renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
        else:
          reject_dict = {"file_name":[name], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          reject_df = pd.concat([reject_df, pd.DataFrame(reject_dict)])
      
  renamed_df.to_csv('renamed_file.csv', index=False)
  reject_df.to_csv('reject_file.csv', index=False)

if __name__ == "__main__":
  for file in glob.glob(pdf_origin_path + "\*.pdf"):
    # pdf_name = file
    read_pdf(file, reader)
  end = time.time()
  print(f'All process successful in {end-start:.2f} sec')

