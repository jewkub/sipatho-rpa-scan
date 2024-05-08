import os, time, sys
from datetime import datetime
from pdf2image import convert_from_path
import pandas as pd
import glob, cv2, easyocr, re, shutil, fitz
import numpy as np
import subprocess, math
from pywinauto import application, mouse
from pywinauto.keyboard import send_keys
from cryptography.fernet import Fernet
from multiprocessing import Process
import multiprocessing

print(multiprocessing.cpu_count())

start = time.time()
main_path = sys.executable if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') else __file__
# path_img = f"{os.path.dirname(main_path)}\\image"
pdf_origin_path = f"{os.path.dirname(main_path)}\\raw"
path_renamed = f"{os.path.dirname(main_path)}\\renamed"
path_done = f"{os.path.dirname(main_path)}\\done"
reader = easyocr.Reader(['en'])

def copy_and_rename(src_path, dest_path, new_name):
  new_path = f"{dest_path}\\{new_name}"
  shutil.move(src_path, new_path)

def chunks(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

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

def remove_empty_page(i, inputfile_paths):
  # inputfile_path = r"D:\git\sipatho-rpa-scan\rename\added_blankpage.pdf"
  # outputfile_path = r"D:\git\sipatho-rpa-scan\rename\editted.pdf"
  for inputfile_path in inputfile_paths:
    temp_name = inputfile_path.split('\\')[-1].split('.')[0]
    # temp_file = f'.\\{temp_name}_temp_pdf.png'
    images = convert_from_path(inputfile_path, fmt='png',poppler_path=f"{os.path.dirname(main_path)}\\poppler\\Library\\bin")
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
    input_pdf.close()
    output_pdf.save(inputfile_path)
    output_pdf.close()

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
  images = convert_from_path(file_name, poppler_path=f"{os.path.dirname(main_path)}\\poppler\\Library\\bin")
  open_cv_image = np.array(images[0])
  img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)

  cropped_image = img[0:300, 1100:1659]
  found = False
  found, name = readOCR(reader=reader, file_name=file_name, image=cropped_image)
  if found:
    print(f"{file_name} Found: " + name)
    renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
    renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
  else:
    image_rotated = cv2.rotate(cropped_image, cv2.ROTATE_180)
    found, name = readOCR(reader=reader, file_name=file_name, image=image_rotated)
    if found:
      print(f"{file_name} Found: " + name)
      renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
      renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
    else:
      cropped_rotated_image = img[2000:2346, 0:600]
      found, name = readOCR(reader=reader, file_name=file_name, image=cropped_rotated_image)
      if found:
        print(f"{file_name} Found: " + name)
        renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
        renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
      else:
        rotated_cropped_rotated_image = cv2.rotate(cropped_rotated_image, cv2.ROTATE_180)
        found, name = readOCR(reader=reader, file_name=file_name, image=rotated_cropped_rotated_image)
        if found:
          print(f"{file_name} Found: " + name)
          renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])
        else:
          print(f"{file_name} Not Found")
          reject_dict = {"file_name":[name], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
          reject_df = pd.concat([reject_df, pd.DataFrame(reject_dict)])

  renamed_df.to_csv('renamed_file.csv', index=False)
  reject_df.to_csv('reject_file.csv', index=False)

def decrypt(token: bytes, key: bytes) -> bytes:
  return Fernet(key).decrypt(token)

if __name__ == "__main__":
  multiprocessing.freeze_support()
  processes = []
  paths_pdf = glob.glob(pdf_origin_path + r"\*.pdf")
  total = len(paths_pdf)
  num_cpu = 5
  chunk_size = math.ceil(total/num_cpu)
  slice = chunks(paths_pdf, chunk_size)
  for i, pdf_path in enumerate(slice):
    p = Process(target=remove_empty_page, args=(i,pdf_path,))
    processes.append(p)
    p.start()

  for process in processes:
    process.join()

  for file in glob.glob(pdf_origin_path + r"\*.pdf"):
    read_pdf(file, reader)
  end = time.time()
  print(f'Rename successful in {end-start:.2f} sec')
  start = time.time()
  # for file in glob.glob(path_renamed + r"\*.pdf"):
  #   print(file)

  login = {
    "login": {
      "user": "gAAAAABmAQ5Q1JcRZ73J3LbYqMPF3p5HJbl6j7B2dd03fNsdDyW2UC42c2i9QpX9Zhj31Gp7lgG37aRIYf6tGX7cOOaSKp5MZA==",
      "password": "gAAAAABmAQ5bVJreT61DvquHmA8KMrxPFhnwG3bK5NwBzOENaVIUJH-P3Rjgh2-ca61ivC2VEzR1WIvqGhLEfFuNcqxhvPUhXA=="
    },
    "key": "qpP1FZ6U1wKUwJgi4LvOsFZAjlAgnWhTtpx80yafbV8="
  }

  renamed_df = pd.read_csv("renamed_file.csv")
  subprocess.run(r"start C:\Users\User\Desktop\HCLAB.LNK", shell=True)
  # subprocess.run(r"start C:\Users\User.DESKTOP-UL2AVPG\Desktop\HCLAB.LNK", shell=True)
  app = application.Application(backend="uia") #.start(r"C:\Users\User.DESKTOP-UL2AVPG\Desktop\HCLABAP.LNK /c start")

  app.connect(title="HCLABAP", timeout=20)

  app.HCLABAP.child_window(title="User Sign In", auto_id="60007", control_type="Window").type_keys(decrypt(login["login"]["user"], login["key"]).decode())
  send_keys("{ENTER}")

  app.HCLABAP.child_window(auto_id="1", control_type="Edit").type_keys(decrypt(login["login"]["password"], login["key"]).decode())
  send_keys("{ENTER}")
  app.connect(title="SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]", timeout=20)
  left = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane10.rectangle().left
  top = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane10.rectangle().top
  #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane12.click_input()
  #x, y = win32api.GetCursorPos()
  mouse.click(coords=(left + 60, top + 10))
  #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Button4"].click_input()

  #print(app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]['     Office']).click_input()

  #app_win32 = application.Application(backend="win64")
  #app_win32.connect(title="SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]", timeout=20)

  #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="Column left",auto_id="UpButton",control_type="Button").GetCheckState()
  
  #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].print_control_identifiers()

  send_keys("^{PGDN}")
  send_keys("^{PGDN}")
  send_keys("^{PGDN}")
  send_keys("{UP}")
  send_keys("^{PGDN}")
  send_keys("{UP}")

  left = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].rectangle().left
  top = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].rectangle().top
  mouse.click(coords=(left - 60, top + 10))
  for i, file in enumerate(glob.glob(path_renamed + r"\*.pdf")):
    filename = file.split("\\")[-1]
    surgicalno = filename.split(".")[0]
    if surgicalno in renamed_df[renamed_df["sending_status"] == True]["file_name"].to_list():
      continue
    send_keys(surgicalno + "{ENTER}")
    #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].click_input()
    app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="Attach File", auto_id="1", control_type="Button").click_input()
    app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="File name:", auto_id="1152", control_type="Edit").type_keys(f"{path_renamed}\\{surgicalno}" + "{DOWN}{ENTER}^{PGDN}{TAB}{TAB}{TAB}{ENTER}")
    # time.sleep(0.5)
    shutil.move(file, f"{path_done}\\{filename}")
    i, c = np.where(renamed_df == surgicalno)
    print(surgicalno)
    print(renamed_df[renamed_df["file_name"] == surgicalno])
    print(renamed_df.iloc[i, 1])
    renamed_df.iloc[i, 1] = True
  renamed_df.to_csv("renamed_file.csv", index=False)
  app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].close()
  app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].close()
  end = time.time()
  print(f'Attach successful in {end-start:.2f} sec')