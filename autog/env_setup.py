import numpy as np 
import cv2 
from PIL import ImageGrab


points = (0,0)

def click(event,x,y,flags,param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points = (x, y)
        

class Enviromet:
    """
    Get the enviromet ready for training
    """
    def __init__(self):
        self.posible_actions = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

    def set_top_left(self):
        global points
        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", click)
        screen = np.array(ImageGrab.grab())
        screen = cv2.resize(screen, (0,0), fx=0.25, fy=0.25)
        while True:
            cv2.circle(screen, points, 3, (0,222,0), 5)
            cv2.imshow("frame", screen)
            ch = cv2.waitKey(1)
            if ch & 0xff == ord('q'):
                break
        cv2.destroyAllWindows()
        self.left , self.top= points[0]*4, points[1]*4

    def set_bottom_right(self):
        global points
        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", click)
        screen = np.array(ImageGrab.grab())
        screen = cv2.resize(screen, (0,0), fx=0.25, fy=0.25)
        while True:
            cv2.circle(screen, points, 3, (0,222,0), 5)
            cv2.imshow("frame", screen)
            ch = cv2.waitKey(1)
            if ch & 0xff == ord('q'):
                break
        cv2.destroyAllWindows()
        self.right, self.bottom = points[0]*4, points[1]*4
