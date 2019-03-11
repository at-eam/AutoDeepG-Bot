import cv2
import numpy as np
from PIL import ImageGrab


points = (0,0)

def click(event,x,y,flags,param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points = (x, y)



def set_top_left():
    """ 
    Get the top left corner of screenshot 
    Press q to contuniue
    """
    global points
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click)
    screen = np.array(ImageGrab.grab())
    screen = cv2.resize(screen, (0,0), fx=0.25, fy=0.25)
    print("Please mark the top left corner and press 'q' ")
    while True:
        cv2.circle(screen, points, 3, (0,222,0), 5)
        cv2.imshow("frame", screen)
        ch = cv2.waitKey(1)
        if ch & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    return points[0]*4, points[1]*4

def set_bottom_right():
    """ 
    Get the bottom right corner of the screenshot 
    press q to contuniue
    """
    global points
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click)
    screen = np.array(ImageGrab.grab())
    screen = cv2.resize(screen, (0,0), fx=0.25, fy=0.25)
    print("Please mark the bottom right corner and press 'q' ")
    while True:
        cv2.circle(screen, points, 3, (0,222,0), 5)
        cv2.imshow("frame", screen)
        ch = cv2.waitKey(1)
        if ch & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()
    return points[0]*4, points[1]*4
