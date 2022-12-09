from mss import mss
import cv2
from PIL import Image
import numpy as np
from time import time, sleep
import pyautogui as pg
import keyboard
import threading

mon = {'top': 100, 'left':100, 'width':800, 'height':512}

sct = mss()
enemy = cv2.imread('D:\Programming Projects\OpenCv Dinosuar Project\cactus.png', cv2.IMREAD_UNCHANGED)
dino = cv2.imread('D:\Programming Projects\OpenCv Dinosuar Project\dino.png', cv2.IMREAD_UNCHANGED)

def add():
    global coord
    while 1:
        sleep(1)
        #coord -= 0.5

dino_pos = (86, 0)
coord = -120

thread = threading.Thread(target=add)
thread.start()

while 1:
    begin_time = time()
    sct_img = sct.grab(mon)
    img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Dino
    try:
        result = cv2.matchTemplate(img_bgr, dino, cv2.TM_SQDIFF_NORMED)

        threshold = 0.1
        locations = np.where(result <= threshold)
        locations = list(zip(*locations[::-1]))

        for loc in locations:
            dino_pos = loc
            top_left = loc
            bottom_right = (top_left[0] + dino.shape[1], top_left[1] + dino.shape[0])
            cv2.rectangle(img_bgr, top_left, bottom_right, (0, 255, 0), cv2.LINE_4)
    except Exception as e:
        print(e)
    
    try:
        result = cv2.matchTemplate(img_bgr, enemy, cv2.TM_SQDIFF_NORMED)

        threshold = 0.175
        locations = np.where(result <= threshold)
        locations = list(zip(*locations[::-1]))

        for loc in locations:
            if((dino_pos[0] - loc[0]) >= coord):
                keyboard.press_and_release("space")
            top_left = loc
            bottom_right = (top_left[0] + enemy.shape[1], top_left[1] + enemy.shape[0])
            cv2.rectangle(img_bgr, top_left, bottom_right, (0, 0, 255), cv2.LINE_4)
    except Exception as e:
        print(e)

    cv2.imshow('test', np.array(img_bgr))
    #print('This frame takes {} seconds.'.format(time()-begin_time))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

thread.join()