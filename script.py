import numpy as np
import cv2
import time

CURR_TIME = time.asctime()

sdThresh = 10

img_index = 0

font = cv2.FONT_HERSHEY_SIMPLEX

def distMap(frame1, framw2):
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

def print_date_time():
    CURR_TIME = time.asctime()
    cv2.putText(frame2, str(CURR_TIME),(10,450),font,0.8,(0,255,0),2, cv2.LINE_AA)
    cv2.putText(frame2,"Enter to pause. Hold ESC to quit.",(10,470), font, 0.6,(255,255,255),1)

cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()

while(True):
    try:
        _, frame3 = cap.read()
        rows, cols, _ = np.shape(frame3)
        dist = distMap(frame1, frame3)
    except:
        print("Camera not found.")
        exit(0)

    frame1 = frame2
    frame2 = frame3

    mod = cv2.GaussianBlur(dist, (9,9), 0)
    _, thresh = cv2.threshold(mod, 100,255,0)
    _, stDev = cv2.meanStdDev(mod)

    if stDev > sdThresh:
        print("Motion detected")
        cv2.putText(frame2, "MD", (0,20), font, 0.8, (0, 255,0),2, cv2.LINE_AA)
        print_date_time()

        frame_name = "./" + str(img_index) + str(".jpg")
        cv2.imwrite(frame_name, frame2)
        print("saved", frame_name)
        img_index += 1

    print_date_time()
    cv2.imshow('Live Video', frame2)

    if cv2.waitKey(1) & 0xFF == 13:
        cv2.putText(frame2, "PAUSED", (230, 260), font, 2, (0, 255,0), 8, cv2.LINE_AA)
        print("PAUSED")
        cv2.imshow('Live video',frame2)
        cv2.waitKey(0)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()