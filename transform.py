import cv2
import numpy as np

# Hard-coded resolution for the video.
image_size = (720, 1280)

def compute_transform_matrices():
    # This is the rectangle I measured on an undistored image from the video
    # where the lanes lines are pretty much centered and straight.
    bottom_left  = (190, 720)
    top_left     = (587, 455)
    top_right    = (703, 455)
    bottom_right = (1130, 720)

    # Location of the rectangle in the original undistorted image.
    src = np.float32([ top_left, top_right, bottom_right, bottom_left ])

    # Leave a margin on the left and right of the top view, making the top-view a 720x720.
    margin = 280
    dst = np.float32([
        [margin,               0],
        [image_size[1]-margin, 0], 
        [image_size[1]-margin, image_size[0]], 
        [margin,               image_size[0]],
    ])

    # Compute the transform matrix and the inverse transform matrix.
    transformMatrix       = cv2.getPerspectiveTransform(src, dst)
    inverseTranformMatrix = cv2.getPerspectiveTransform(dst, src)

    return transformMatrix, inverseTranformMatrix

def compute_top_view(undistorted, transformMatrix):
    topview = cv2.warpPerspective(undistorted, transformMatrix, (image_size[1], image_size[0]), flags=cv2.INTER_LINEAR)
    return topview

def compute_unwarped_view(topview, inverseTransformMatrix):
    unwarped = cv2.warpPerspective(topview, inverseTransformMatrix, (image_size[1], image_size[0]), flags=cv2.INTER_LINEAR)
    return unwarped

if __name__ == '__main__':
    import sys

    # Compute the perspective transform matrix and its inverse.
    transformMatrix, inverseTransformMatrix = compute_transform_matrices()

    # Read an undistorted image.
    undistorted = cv2.imread(sys.argv[1])

    # Use the transform matrix to compute the top-view, and save it.
    topview = compute_top_view(undistorted, transformMatrix)
    cv2.imwrite(sys.argv[2], topview)

    # Use the inverse transform matrix to got from the top-view to the
    # undistorted image.
    unwarped = compute_unwarped_view(topview, inverseTransformMatrix)
    cv2.imwrite(sys.argv[3], unwarped)
