import numpy as np 
import cv2 
from PIL import ImageGrab
import time 
from autog.control import get_mouse_location, move_mouse
from collections import deque, namedtuple
from autog.train_pytorch import play_mouse

from autog.utils import set_bottom_right, set_top_left



class Environment:

    def set_top_left():
        raise NotImplementedError
    def set_bottom_right():
        raise NotImplementedError
    def start_recording():
        raise NotImplementedError
    def save_memory():
        raise NotImplementedError
    def load_memory():
        raise NotImplementedError
    def memory():
        raise NotImplementedError
    def play():
        raise NotImplementedError


class Mouse_Control_Env(Environment):
    def __init__(self, 
    mouse_control = False,
    max_memory = 10000):
        """ 
        Get the Environment ready for training for
        environments controled with only mouse

        Params:
        ======
        mouse_control: Does env use mouse control 
        max_memory: maximum data stored during recording 
        
        """
        self.posible_actions = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

        self.mouse_control = mouse_control
        self.state_memory = deque(maxlen = max_memory)
        self.mouse_action_memory = deque(maxlen = max_memory)

        self.mouse_model = None

        self.mouse_std = None
        self.mouse_mean = None

    def set_screen(self):
        self.left , self.top = set_top_left()
        self.right, self.bottom = set_bottom_right()

    def start_recording(self, t = 100):
        """
        Start creatating your dataset,
        functions stores both state from the screen and 
        actions from mouse and saves them

        Params:
        =======
        t: number of examples that will be stored 
        """
        while  len(self.state_memory) <= t:
            screen = ImageGrab.grab(bbox=(self.left , self.top, self.right, self.bottom))
            screen = np.array(screen.resize((80,80)))
            self.state_memory.append(screen)

            mouse_location = get_mouse_location()
            self.mouse_action_memory.append(mouse_location)


    def save_memory(self, filename):
        """
        saves the states and actions memory to filename path
        """
        np.save(filename + "states.npy",np.array(self.state_memory))
        np.save(filename + "mouse_action.npy", np.array(self.mouse_action_memory))
        np.save(filename+"info.npy", np.array([self.posible_actions,self.top,self.bottom,self.right,self.left]))


    def load_memory(self, filename):
        """
        loads memory from filename path
        """
        self.state_memory = np.load(filename + "states.npy")
        self.mouse_action_memory = np.load(filename + "mouse_action.npy")
        info = np.load(filename + "info.npy")
        self.posible_actions = info[0]
        self.top = info[1]
        self.bottom = info[2]
        self.right = info[3]
        self.left = info[4]


    def memory(self):
        """
        Returns truple: states and mouse_actions 
        """
        states = np.array(self.state_memory)[:,:,:,:3]/255

        m_actions = np.array(self.mouse_action_memory)
        self.mouse_std = np.std(m_actions)
        self.mouse_mean = np.mean(m_actions)
        m_actions = (m_actions-self.mouse_mean)/self.mouse_std

        return states, m_actions
        

    def play(self):
        """
        Game bot starts playing itself
        """
        while True:
            screen = ImageGrab.grab(bbox=(self.left , self.top, self.right, self.bottom))
            screen = np.array(screen.resize((80,80)))[:,:,:3]/255
            screen = np.reshape(screen, [1,80,80,3])
            screen = np.transpose(screen, (0, 3, 1, 2))
            if self.mouse_control:
                mouse = play_mouse(self.mouse_model, screen)
                mouse = (mouse*self.mouse_std) + self.mouse_mean
                move_mouse(mouse[0][0], mouse[0][1])


class Keyboard_Control_Env():

    def __init__(self,  max_memory = 10000):
        """ 
        Get the Environment ready for training for
        environments controled with keyboard

        Params:
        ======
        keyboard_control: Does env use keyboard control 
        max_memory: maximum data stored during recording 
        
        """
        self.posible_actions = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

        self.state_memory = deque(maxlen = max_memory)
        self.keyboard_action_memory = deque(maxlen = max_memory)

        self.keyboard_model = None
        # DID YOU FUCKING READ THE CODE :D 
        self.keyboard_std = None
        self.keyboard_mean = None

    def set_screen(self):
        self.left , self.top = set_top_left()
        self.right, self.bottom = set_bottom_right()

    def start_recording(self, t = 100):
        """
        Start creatating your dataset,
        functions stores both state from the screen and 
        actions from the keyboard and saves them

        Params:
        =======
        t: number of examples that will be stored 
        """

        while len(self.state_memory) <= t:
            screen = ImageGrab.grab(bbox=(self.left , self.top, self.right, self.bottom))
            screen = np.array(screen.resize((80,80)))
            self.state_memory.append(screen)

            self.keyboard_action_memory = 

