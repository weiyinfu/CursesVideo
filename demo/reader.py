from os.path import *

import cv2

filepath = join(dirname(abspath(__file__)), '..', 'you belong with me.mp4')
x = cv2.VideoCapture(filepath)
print(x.isOpened())
while 1:
    v, frame = x.read()
    print(type(v), type(frame))
    import matplotlib.pyplot as plt

    plt.imshow(frame)
    plt.show()
    input()
