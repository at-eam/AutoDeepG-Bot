"""
To do:
======

Mouse
------
def get_if_clicked 
def move
def click


Keybord
------
def get_pressed_buttons 
def 

"""


from pynput.mouse import Button, Controller as Mouse
from pynput.keyboard import Key, Controller as Keyboard

mouse = Mouse()

def get_mouse_location():
    x, y = mouse.position
    return [x,y] 
    

