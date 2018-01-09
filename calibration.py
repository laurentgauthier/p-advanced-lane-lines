import numpy as np
import cv2

def camera_calibration(images):
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    
    
    # Step through the list and search for chessboard corners
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
    
        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

    # Now compute the camera parameters
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return mtx, dist

def camera_undistort(image, mtx, dist):
    return cv2.undistort(image, mtx, dist, None, mtx)
    
if __name__ == '__main__':
    import sys
    import glob

    # Make a list of calibration images
    images = glob.glob('camera_cal/calibration*.jpg')

    mtx, dist = camera_calibration(images)

    # Load a distorted image and undistort it.
    distorted = cv2.imread(sys.argv[1])
    undistorted = camera_undistort(distorted, mtx, dist)
    cv2.imwrite(sys.argv[2], undistorted)
