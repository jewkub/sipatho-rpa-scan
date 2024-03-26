import subprocess
from pywinauto import application, Desktop, mouse
from pywinauto.keyboard import send_keys
from cryptography.fernet import Fernet
import win32api, glob
import time
import pandas as pd
import numpy as np

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

if __name__ == "__main__":
    login = {
      "login": {
        "user": "gAAAAABmAQ5Q1JcRZ73J3LbYqMPF3p5HJbl6j7B2dd03fNsdDyW2UC42c2i9QpX9Zhj31Gp7lgG37aRIYf6tGX7cOOaSKp5MZA==",
        "password": "gAAAAABmAQ5bVJreT61DvquHmA8KMrxPFhnwG3bK5NwBzOENaVIUJH-P3Rjgh2-ca61ivC2VEzR1WIvqGhLEfFuNcqxhvPUhXA=="
      },
      "key": "qpP1FZ6U1wKUwJgi4LvOsFZAjlAgnWhTtpx80yafbV8="
    }

    renamed_df = pd.read_csv("renamed_file.csv")
    
    subprocess.run(r"start C:\Users\User.DESKTOP-UL2AVPG\Desktop\HCLABAP.LNK", shell=True)
    app = application.Application(backend="uia") #.start(r"C:\Users\User.DESKTOP-UL2AVPG\Desktop\HCLABAP.LNK /c start")

    app.connect(title="HCLABAP", timeout=20)

    app.HCLABAP.child_window(title="User Sign In", auto_id="60007", control_type="Window").type_keys(decrypt(login["login"]["user"], login["key"]).decode())
    send_keys("{ENTER}")

    app.HCLABAP.child_window(auto_id="1", control_type="Edit").type_keys(decrypt(login["login"]["password"], login["key"]).decode())
    send_keys("{ENTER}")
    app.connect(title="SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]", timeout=20)
    left = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane12.rectangle().left
    top = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane12.rectangle().top
    #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].Pane12.click_input()
    #x, y = win32api.GetCursorPos()
    mouse.click(coords=(left + 60, top + 10))
    #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Button4"].click_input()

    #print(app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]['     Office']).click_input()

    #app_win32 = application.Application(backend="win64")
    #app_win32.connect(title="SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]", timeout=20)

    #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="Column left",auto_id="UpButton",control_type="Button").GetCheckState()
    
    #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].print_control_identifiers()

    
    ########## keep #######################
    send_keys("^{PGDN}")
    send_keys("^{PGDN}")
    send_keys("^{PGDN}")
    send_keys("{UP}")
    send_keys("^{PGDN}")
    send_keys("{UP}")

    left = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].rectangle().left
    top = app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].rectangle().top
    mouse.click(coords=(left - 60, top + 10))
    #mouse.click(coords=(560, 685))
    #print(app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].rectangle())
    for i, file in enumerate(glob.glob(r"renamed\*.pdf")):
        surgicalno = file.split("\\")[-1].split(".")[0]
        if surgicalno in renamed_df[renamed_df["sending_status"] == True]["file_name"].to_list():
            continue
        send_keys(surgicalno + "{ENTER}")
        #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Pane84"].click_input()
        app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="Attach File", auto_id="1", control_type="Button").click_input()
        if i == 0:
            app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Look in:ComboBox"].click_input()
            app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"]["Look in:ComboBox"].Desktop.click_input()
            #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].print_control_identifiers()
            #app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="Look in:", auto_id="1091", control_type="Text").type_keys("desktop")
            app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="File name:", auto_id="1152", control_type="Edit").type_keys("ไฟล์ต่างๆบนหน้าจอ{ENTER}")
            app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="File name:", auto_id="1152", control_type="Edit").type_keys("rename{ENTER}")
            app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="File name:", auto_id="1152", control_type="Edit").type_keys("renamed{ENTER}")
        app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].child_window(title="File name:", auto_id="1152", control_type="Edit").type_keys(surgicalno + "{DOWN}{ENTER}^{PGDN}{TAB}{TAB}{TAB}{ENTER}")

        i, c = np.where(renamed_df == surgicalno)
        print(surgicalno)
        print(renamed_df[renamed_df["file_name"] == surgicalno])
        print(renamed_df.iloc[i, 1])
        renamed_df.iloc[i, 1] = True
    renamed_df.to_csv("renamed_file.csv", index=False)
    app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].close()
    app["SIRIRAJ HOSPITAL - [10029665 : เพ็ญศรี เนียมยิ้ม]"].close()
    """windows = Desktop(backend="uia").windows()

    for window in windows:
        print(window.window_text())
        print("-------------")"""

    
