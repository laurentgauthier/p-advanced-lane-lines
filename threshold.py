import cv2
import numpy as np

def threshold_image(image):
    # Blur the image
    kernel_size = 3
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    R = blurred[:,:,1] # Good for white lines.
    B = blurred[:,:,1] # Good for yellow lines.
    RB = cv2.addWeighted(R, 0.5, B, 0.5, 0.0)

    # Extract the S channel.
    hls = cv2.cvtColor(blurred, cv2.COLOR_RGB2HLS)
    S = hls[:,:,2]

    # Run an adaptive Gaussian threshold on the combination of S and R+B.
    binary = cv2.adaptiveThreshold(cv2.addWeighted(S, 0.5, RB, 0.5, 0.0),\
                                   255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY, 33, -10)
    return binary

if __name__ == '__main__':
    import sys

    image = cv2.imread(sys.argv[1])
    binary = threshold_image(image)
    color = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(sys.argv[2], color)
