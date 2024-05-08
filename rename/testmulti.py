# import pdf2image
import os
from pdf2image import convert_from_path
# import pytesseract as tess
# Importing the Image module from the PIL package to work with images
from PIL import Image
import pandas as pd
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import easyocr
import re, time
import shutil
import sys, fitz
import math
from multiprocessing import Process, Pool
import glob

start_all = time.time()

path_img = r"D:\git\sipatho-rpa-scan\rename\image"
pdf_origin_path = r"D:\git\sipatho-rpa-scan\rename\raw"
path_renamed = r"D:\git\sipatho-rpa-scan\rename\renamed"
reader = easyocr.Reader(['en'])
crop_name = "image.png"

def chunks(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

def check_page(page):
  text = page.get_text()
  return len(text.strip()) == 0

def remove_empty_page(i, inputfile_paths):
  # inputfile_path = r"D:\git\sipatho-rpa-scan\rename\added_blankpage.pdf"
  # outputfile_path = r"D:\git\sipatho-rpa-scan\rename\editted.pdf"
  for inputfile_path in inputfile_paths:
    temp_name = inputfile_path.split('\\')[-1].split('.')[0]
    temp_file = f'.\\{temp_name}_temp_pdf.png'
    images = convert_from_path(inputfile_path, fmt='png',poppler_path=r"C:\Users\jewna\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin")
    input_pdf = fitz.open(inputfile_path)
    output_pdf = fitz.open()
    for pgno in range(input_pdf.page_count):
      # print(pgno)
      page = input_pdf[pgno]
      if not check_page(page):
        output_pdf.insert_pdf(input_pdf,from_page=pgno,to_page = pgno)
      else:
        print('Job id: '+str(i),'\n','file: ' + str(temp_name) + ', Page No: ' + str(pgno))
        # pix = page.get_pixmap()
        # pix.save(temp_file)
        img_page = images[pgno]
        open_cv_image = np.array(img_page)
        img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = img[0:800, 700:1200]
        # cropped_image.save(temp_file)
        # cv2.imwrite('cropped' + str(pgno) + '.jpg', cropped_image)
        result = reader.readtext(cropped_image, detail=0)
        # print('Success to read')
        # print (result)
        if len(result) > 0:
          output_pdf.insert_pdf(input_pdf,from_page=pgno,to_page = pgno)
    output_pdf.save(inputfile_path + "noblank.pdf")
    output_pdf.close()
    input_pdf.close()
  
if __name__ == "__main__":
  processes = []
  paths_pdf = glob.glob(pdf_origin_path + r"\*.pdf")
  total = len(paths_pdf)
  num_cpu = 5
  chunk_size = math.ceil(total/num_cpu)
  slice = chunks(paths_pdf, chunk_size)
  for i,pdf_path in enumerate(slice):
    p = Process(target=remove_empty_page, args=(i,pdf_path,))
    processes.append(p)
    p.start()
  
  for process in processes:
    process.join()

  end_all = time.time()

  print('That took {} second for all processes'.format(end_all-start_all))