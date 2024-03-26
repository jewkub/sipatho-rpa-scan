import os, time, sys
from datetime import datetime
from pdf2image import convert_from_path
import pandas as pd
import glob, cv2, easyocr, re, shutil, fitz
import numpy as np

start = time.time()
path_img = f"{os.path.dirname(__file__)}\\image"
pdf_origin_path = f"{os.path.dirname(__file__)}\\raw"
path_renamed = f"{os.path.dirname(__file__)}\\renamed"
reader = easyocr.Reader(['en'])

def copy_and_rename(src_path, dest_path, new_name):
  new_path = f"{dest_path}\\{new_name}"
  shutil.move(src_path, new_path)

def readOCR(reader: easyocr.Reader, file_name: str, image: np.ndarray):
  result = reader.readtext(image)
  found = False
  for detection in result:
    match = re.search("[A-Z]{1,3}[0-9]{8}", detection[1])
    if match:
      new_name = match.group(0)
      copy_and_rename(file_name, path_renamed, new_name+".pdf")
      found = True
      break

  # if found:
  #   return True, new_name
  # else:
  #   return False, file_name
  return (True, new_name) if found else (False, file_name)

# For checking whether the page is empty or not.
def check_page(page):
  text = page.get_text()
  return len(text.strip()) == 0

def remove_empty_page(inputfile_path):
  # inputfile_path = r"D:\git\sipatho-rpa-scan\rename\added_blankpage.pdf"
  # outputfile_path = r"D:\git\sipatho-rpa-scan\rename\editted.pdf"
  temp_file = r'.\temp_pdf.png'
  images = convert_from_path(inputfile_path, fmt='png',poppler_path=r"C:\Users\jewna\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin")
  input_pdf = fitz.open(inputfile_path)
  output_pdf = fitz.open()
  for pgno in range(input_pdf.page_count):
    # print(pgno)
    page = input_pdf[pgno]
    if not check_page(page):
      output_pdf.insert_pdf(input_pdf,from_page=pgno,to_page = pgno)
    else:
      print('Page No:',pgno)
      # pix = page.get_pixmap()
      # pix.save(temp_file)
      img_page = images[pgno]
      img_page.save(temp_file)
      result = reader.readtext(temp_file)
      print('Success to read')
      if len(result) > 0:
        output_pdf.insert_pdf(input_pdf,from_page=pgno,to_page = pgno)
  output_pdf.save(inputfile_path + "noblank.pdf")
  output_pdf.close()
  input_pdf.close()

def read_pdf(file_name, reader):
  if os.path.exists("renamed_file.csv"):
    renamed_df = pd.read_csv("renamed_file.csv")
  else:
    renamed_df = pd.DataFrame(columns=["file_name", "sending_status", "timestamp"])

  if os.path.exists("reject_file.csv"):
    reject_df = pd.read_csv("reject_file.csv")
  else:
    reject_df = pd.DataFrame(columns=["file_name", "timestamp"])

  # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format#comment46123650_14140796
  images = convert_from_path(file_name, poppler_path=f"{os.path.dirname(__file__)}\\poppler\\Library\\bin")
  open_cv_image = np.array(images[0])
  img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)

  cropped_image = img[0:300, 1100:1659]
  found = False
  found, name = readOCR(reader=reader, file_name=file_name, image=cropped_image)
  if found:
    print(f"{file_name} Found")
    renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
    renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
  else:
    image_rotated = cv2.rotate(cropped_image, cv2.ROTATE_180)
    found, name = readOCR(reader=reader, file_name=file_name, image=image_rotated)
    if found:
      print(f"{file_name} Found")
      renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
      renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
    else:
      cropped_rotated_image = img[2000:2346, 0:600]
      found, name = readOCR(reader=reader, file_name=file_name, image=cropped_rotated_image)
      if found:
        print(f"{file_name} Found")
        renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
        renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
      else:
        rotated_cropped_rotated_image = cv2.rotate(cropped_rotated_image, cv2.ROTATE_180)
        found, name = readOCR(reader=reader, file_name=file_name, image=rotated_cropped_rotated_image)
        if found:
          print(f"{file_name} Found")
          renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
        else:
          print(f"{file_name} Not Found")
          reject_dict = {"file_name":[name], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          reject_df = pd.concat([reject_df, pd.DataFrame(reject_dict)])

  renamed_df.to_csv('renamed_file.csv', index=False)
  reject_df.to_csv('reject_file.csv', index=False)

if __name__ == "__main__":
  for file in glob.glob(pdf_origin_path + r"\*.pdf"):
    remove_empty_page(file)
    read_pdf(file, reader)
  end = time.time()
  print(f'Rename successful in {end-start:.2f} sec')
  # for file in glob.glob(path_renamed + r"\*.pdf"):
  #   print(file)
