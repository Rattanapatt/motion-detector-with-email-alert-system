# Motion Detector

## Overview
This is a motion detector app.

## Using library
### 1. cv2 (phthon-cv2)
for working with image. From creating image and getting image from the webcam
### 2. time
to work with time
### 3. datetime
to work with datetime format. This makes working with time more convenient.
### 4. glob
to find location of the file
### 5. os
to get access to system environment variable
### 6. threading
this makes the program able to run some particular parts paralelly 
### 7. smtplib
this is for sending an email
### 8. imghdr
this is to tell the program the type of image
### 9. email.message
to consturct an email content structure.

***

## Motion Detection
This is the code part for motion detection.

### Video Capture Initialization
```python
video = cv2.VideoCapture(1, cv2.CAP_DSHOW) 
t.sleep(1)
```
- `cv2.VideoCapture()`: Opens the webcam. The number 1 in the sample code means select camera number 1 in case there are multiple camera connected. The cv2.CAP_DSHOW argument ensures the camera is initialized faster (Not sure why).
- `t.sleep()`: Use for delay execution of the code. In this case the number is 1 which means 1-second delay. It is to give the camera time to start.

### Main loop to keep the program operate
```python
while True:
    check, frame = video.read()
    status = 0
```
- `check, frane = video.read()`: `check` stores boolean data (True/False) and `frame` stores image data
- `status`: This variable stores the simplified motion signal. which 0 is no motion and 1 is motion.

### Grayscale Conversion and Smoothing
```python
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
```
- `cv2.cvtColor()`: It is a simplified method to convert the color of the frame into something. In this case, `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)` intends to convert the color to grayscale.
- `cv2GaussianBlur(gray_frame, (21, 21), 0)`: This blurs the frame using the Gaussian method. The argument that can be adjusted is the number inside the parentheses, representing the size of the kernel used for blurring, which is `(21, 21)`. Both number should be the same and the more number is the blurry it gets.

### First Frame Initialization
```python
if first_frame is None:
    first_frame = gray_frame_gau
```
- This is just to initiate the first_frame to compare it with the subsequent frames for detecting chages, which refers to motions.

### Delta Frame (Motion Detection)
```python
delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
```
- `cv2.abbsdiff`: This function computes the absolute difference. between current frame and the first frame.

### Thresholding and Contours
```python
thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
```
- `cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]`: The values in this function are ordered as follows. `(source, thresholdValue, maxVal, thresholdingTechnique)`

    - `source`: source of the processing image
    - `thresholdValue`: Indicate the value(i). Any value that below and above that value(i) which pixel values will change accordingly.
    - `maxVal`: Maximum value that can be in each pixels. In this case, 255 means White (The pic in this state is already grayscale.).
    - `thresholdingTechnique`: It's to indicate the technique to use.

        - `cv.TRESH_BINARY`
        - `cv.THRES_BINARY_INV`
        - `cv.THRES_TRUNC`
        - `cv.THRES_TOZERO`
        - `cv.THRES_TOZERO_INV`

### Display date and time to the screen
```python
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
time_arr = {"current_date": current_date, "current_time": current_time}

cv2.putText(frame, current_date, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
cv2.putText(frame, current_time, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
```
- Set up time to show on the screen.

### Contour Detection
```python
contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- `cv2.findContours`: Finds the contours of white areas in the thresholded image. Contours are the boundaries of detected objects.

### Object Filtering and Detection
```python
for contour in contours:
    if cv2.contourArea(contour) < 5000:
        continue
    x, y, w, h = cv2.boundingRect(contour)
    rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    if rectangle.any():
        status = 1
```
- `cv2.contourArea`: Filters out small contours, ignoring objects smaller than a certain area (5000 pixels).
- `cv2.boundingRect`: Draws a rectangle around the detected object. This method/function return coordinate and size.
- `cv2.rectangle`: Highlights the moving object in a green rectangle.
- If an object is detected, the status is set to 1, indicating motion.

***

## Capturing and Emailing Image:
```python
cv2.imwrite(f"images/{count}.png", frame)
```
- `cv2.imwrite`: Saves the current frame with the detected object to the "images" folder.
```python
status_list.append(status)
status_list = status_list[-2:]

if status_list[0] == 1 and status_list[1] == 0:
    send_email_thread = Thread(target=send_email, args=(image_with_obj, time_arr, ))
    send_email_thread.daemon = True
    send_email_thread.start()
```
- Shorten the status_list with `status_list = status_list[-2:]`
- `if` statement perform the sending emal task if the motion is detected.
- `thread` is used for paralel task so when the image is captured and sent, the camera won't stop.

***

## Display and Exit
```python
cv2.imshow("Video", frame)
key = cv2.waitKey(1)
if key == ord("q"):
    clean_folder()
    break
```
- `cv2.imshow`: Display the video window with the window title name "Video"
- `cv2.waitKey(1)`: In this case, key "q" is used to clean the image folder and exit the program.
```python
video.release()
```
- Release the camera.






