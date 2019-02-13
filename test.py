from autog.env_setup import Enviromet
import cv2
import numpy as np 
from PIL import ImageGrab


env = Enviromet()

env.set_top_left()

env.set_bottom_right()


screen = np.array(ImageGrab.grab(bbox=(env.left , env.top, env.right, env.bottom)))


while True:
    cv2.imshow("Screen", screen)

    ch = cv2.waitKey(1)
    if ch & 0xff == ord('q'):
        break
cv2.destroyAllWindows()



