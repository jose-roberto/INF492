import numpy as np
import cv2 as cv
import glob
# Load previously saved data
with np.load('calibration_data.npz') as X:
     mtx, dist = [X[i] for i in ('mtx','dist')]

def draw(img, corners, imgpts):
    imgpts = np.asarray(imgpts).reshape(-1, 2)
    
    corner = (int(float(corners[0][0][0])), int(corners[0][0][1]))
    
    pts0 = (int(float(imgpts[0][0])), int(float(imgpts[0][1])))
    pts1 = (int(float(imgpts[1][0])), int(float(imgpts[1][1])))
    pts2 = (int(float(imgpts[2][0])), int(float(imgpts[2][1])))

    img = cv.line(img, corner, pts0, (255,0,0), 5)
    img = cv.line(img, corner, pts1, (0,255,0), 5)
    img = cv.line(img, corner, pts2, (0,0,255), 5)
    return img

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)


for fname in glob.glob('captured_frame_*.png'):
    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (7,7),None)
    if ret == True:
        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        # Find the rotation and translation vectors. 
        ret,rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
        # project 3D points to image plane
        imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
        
        img = draw(img,corners2,imgpts)
        cv.imshow('img',img)

        k = cv.waitKey(0) & 0xFF
        
cv.destroyAllWindows()