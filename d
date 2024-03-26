if not found:
    image_rotated = cv2.rotate(cropped_image, cv2.ROTATE_180)
    found, name = readOCR(reader=reader, file_name=file_name, image=image_rotated)
  if not found:
    cropped_rotated_image = img[2000:2346, 0:600]
    found, name = readOCR(reader=reader, file_name=file_name, image=cropped_rotated_image)
  if not found:
    rotated_cropped_rotated_image = cv2.rotate(cropped_rotated_image, cv2.ROTATE_180)
    found, name = readOCR(reader=reader, file_name=file_name, image=rotated_cropped_rotated_image)
  if not found:
    print(f"{file_name} Not Found")
    reject_dict = {"file_name":[name], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
    reject_df = pd.concat([reject_df, pd.DataFrame(reject_dict)])
  else:
    print(f"{file_name} Found")
    renamed_dict = {"file_name":[name], "sending_status":[False], "timestamp": [datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")]}
    renamed_df = pd.concat([renamed_df, pd.DataFrame(renamed_dict)])