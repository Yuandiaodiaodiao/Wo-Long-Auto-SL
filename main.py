# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
from get_game import get_GAME
from keyboardsim import press_str, pressdownfor_str

from cnocr import CnOcr, consts
from utils import castimg


def perpareimg(img, argmap, show=False):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img720p = img
    # img=cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)
    imggray = img720p
    if show:
        plt.subplot(221)
        plt.imshow(imggray)

    h, w = imggray.shape[0:2]

    img_code_matrix = castimg(imggray, argmap, h, w)
    if show:
        plt.subplot(222)
        plt.imshow(img_code_matrix)
        plt.show()
    return img_code_matrix


ocr = CnOcr()






def save(x):
    try:
        with open('WOLONG_ARM.txt', 'a', encoding='utf-8')as f:
            f.write(x)
            f.write('\n')
    except:
        pass


def getWoLong():
    imgo = get_GAME("Wo Long: Fallen Dynasty")
    img720p = cv2.resize(imgo, (1920, 1080))
    return img720p
def findContinue():
    img=getWoLong()
    h = 0.05
    t = 0.875
    l = 0.9
    w = 0.08
    imgcut = [t, t + h, l, l + w]
    img = perpareimg(img, imgcut, False)
    res = ocr.ocr(img)
    arr=list(map(lambda x:"".join(x),res))
    s="".join(arr)
    return ('继' in s) or('续' in s) or ('A' in s)

def readArmor():
    img720p=getWoLong()
    h=0.15
    t=0.605
    l=0.391
    w=0.2
    imgcut = [t, t+h, l, l+w]
    img = perpareimg(img720p, imgcut, False)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            col=img[i][j]
            maxc=max(col[0],col[1],col[2])
            img[i][j][0]=maxc
            img[i][j][1]=maxc
            img[i][j][2]=maxc


    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    img2=cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, -80)
    plt.imshow(img2,cmap='Greys_r')
    plt.show()
    res = ocr.ocr(img2)

    arr=list(map(lambda x:"".join(x),res))
    return arr


def sl_once():
    press_str('esc')
    time.sleep(0.5)
    press_str('esc')
    time.sleep(0.3)
    for i in range(5):
        time.sleep(0.03)
        press_str('d')
    
    press_str('k')
    time.sleep(0.5)
    press_str('w')
    time.sleep(0.2)
    press_str('k')
    time.sleep(0.2)
    press_str('w')
    time.sleep(0.2)
    press_str('k')

    time.sleep(5)
    for i in range(10*10):
        time.sleep(0.1)
        press_str('k')
    while not findContinue():
        time.sleep(0.5)

    time.sleep(0.5)
    press_str('k')
    time.sleep(1)
    pressdownfor_str('d',1.3)
    pressdownfor_str('w',0.5)
    for i in range(3):
        time.sleep(0.3)
        press_str('e')
    time.sleep(1)
    press_str('esc')
    time.sleep(0.5)
    press_str('k')
    time.sleep(0.5)
    press_str('d')
    press_str('d')
    time.sleep(0.1)
    res=readArmor()
    want=["套装效果","道君之"]

    allEffect=",".join(res)
    print(allEffect)
    save(allEffect)

    for i in want:
        if i in allEffect:
            print("出货")
            raise Exception("找到了")
    

def InfinityX():
    while True:
        sl_once()
        time.sleep(1)



if __name__ == '__main__':
    from keyboard_listener import KListener

    l = KListener()

    # 自动sl
    l.bindKeyAsync('f8', InfinityX,"自动SL")

    # 截图debug
    l.bindKeyAsync('f9', readArmor)

    # 一轮装备
    l.bindKeyAsync('f7', sl_once)

    # 找继续按钮
    l.bindKeyAsync('f6', findContinue)
    l.join()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
