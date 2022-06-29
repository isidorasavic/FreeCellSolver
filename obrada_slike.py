import numpy as np
import cv2 # OpenCV biblioteka
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = 16, 12

img = cv2.imread('dataset/training/4169455.jpg')
plt.imshow(img)



