import numpy as np 
import cv2 
from PIL import ImageGrab
import time 
from autog.control import get_mouse_location
from collections import deque, namedtuple


points = (0,0)

def click(event,x,y,flags,param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points = (x, y)
        

class Environment:
    def __init__(self, 
    mouse_control = False,
    keyboard_control = False, 
    max_memory = 10000):

        """ 
        Get the Environment ready for training 

        Params:
        ======

        """
        self.posible_actions = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

        self.state_memory = deque(maxlen = max_memory)
        self.mouse_action_memory = deque(maxlen = max_memory)
        self.keyboard_action_memory = deque(maxlen = max_memory)

        self.model = None

        self.mouse_control = mouse_control
        self.mouse_std = None
        self.mouse_mean = None
        self.keyboard_control = keyboard_control

    def set_top_left(self):
        """ Get the top left corner of screenshot """
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
        """ Get the bottom left corner of the screenshot """
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


    def start_recording(self, t = 100):
        while  len(self.state_memory) <= t:
            screen = np.array(ImageGrab.grab(bbox=(self.left , self.top, self.right, self.bottom)))
            self.state_memory.append(screen)

            if self.mouse_control:
                mouse_location = get_mouse_location()
                self.mouse_action_memory.append(mouse_location)

            if self.keyboard_control:
                # Todo
                NotImplementedError


    def save_memory(self, filename):
        np.save(filename + "states.npy",np.array(self.state_memory))
        if self.mouse_control:
            np.save(filename + "mouse_action.npy", np.array(self.mouse_action_memory))
        if self.keyboard_control:
            np.save(filename + "keyboard_action.npy", np.array(self.keyboard_action_memory))

    def load_memory(self, filename):
        self.state_memory = np.load(file_name + "states.npy")
        if self.mouse_control:
            self.mouse_action_memory = np.load(filename + "mouse_action.npy")
        if self.keyboard_control:
            self.keyboard_action_memory = np.load(filename + "keyboard_action.npy")

    def memory(self):
        """
        Returns truple: states , mouse_actions and keyboard actions 
        """
        states = np.array(self.state_memory)[:,:,:,:3]/255
        
        m_actions = np.array(self.mouse_action_memory)
        self.mouse_std = np.std(m_actions)
        self.mouse_mean = np.mean(m_actions)
        m_actions = (m_actions-self.mouse_mean)/self.mouse_std

        k_actions = np.array(self.keyboard_action_memory)

        if self.mouse_control and self.keyboard_control:
            return states, m_actions, k_actions
        elif self.mouse_control:
            return states, m_actions, np.array([])
        elif self.keyboard_control:
            return states, np.array([]), k_actions

