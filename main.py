import cv2
import time as t
from datetime import datetime
from emailing import send_email, clean_folder
import glob
from threading import Thread

video = cv2.VideoCapture(1, cv2.CAP_DSHOW) # parameter needs integer of number of camera
# cv2.CAP_DSHOW makes the camera open faster
t.sleep(1)
first_frame = None
status_list = []
count = 0

while True:
    check, frame = video.read() # check is bool, frame is array
    status = 0
    
    # turn pic to gray scale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    # init first_frame
    if first_frame is None:
        first_frame = gray_frame_gau
    
    # find delta frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    
    # scope object and filter noise
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] # thresold can be changed
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    
    # Display the date and time
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    time_arr = {"current_date": current_date, "current_time": current_time}
    
    cv2.putText(frame, current_date, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, current_time, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # create contour
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 5000: # this calue can be changes
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_image = glob.glob("images/*.png")
            index = len(all_image) // 2
            image_with_obj = all_image[index]
    
    status_list.append(status)
    status_list = status_list[-2:]
    
    if status_list[0] == 1 and status_list[1] == 0:
        send_email_thread = Thread(target=send_email, args=(image_with_obj, time_arr, ))
        send_email_thread.daemon = True
        
        send_email_thread.start()
    
    # Visual the screen    
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    
    if key == ord("q"):
        clean_folder()
        break
    
video.release()