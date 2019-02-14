from autog.env_setup import Environment
import cv2
import numpy as np 
from PIL import ImageGrab


env = Environment(mouse_control=True)

env.set_top_left()

env.set_bottom_right()

env.start_recording(t=5)

s, m, k = env.memory()


print(s.shape, m.shape)