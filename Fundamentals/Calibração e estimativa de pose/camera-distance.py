import cv2
import numpy as np
import os
import time

### CHANGE ###
pattern_size = (7, 7)   # Change to match your chessboard
marker_size = 2.8       # Change to match your marker size in centimeters
devide_id = 0           # Change the device id
fps = 30.0              # change the fps to match your device
height = 480.0          # change the frame height to match your device
width = 640.0           # change the frame width to match your device
calibration_file = 'calibration_data.npz' # change the relative path
### CHANGE END ###

# Check available formats
# v4l2-ctl -d /dev/video0 --list-formats-ext

def draw(img, corners, imgpts):
    corners = (np.rint(corners)).astype(int)
    imgpts = (np.rint(imgpts)).astype(int)
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


cmd = 'v4l2-ctl --set-ctrl=focus_auto=0,white_balance_temperature_auto=0,constrat=81,saturation=3'
os.system(cmd)
time.sleep(1)

# Initialize the camera capture
cap = cv2.VideoCapture(devide_id) 

cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

if ( cap.get(cv2.CAP_PROP_FRAME_WIDTH) != width ) or (height != cap.get(cv2.CAP_PROP_FRAME_HEIGHT) ) or ( fps != cap.get(cv2.CAP_PROP_FPS) ) :
    print( "ERRO na configuração da câmera." )
    print( f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}" )
    print( f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}" )
    print( f"FPS: {cap.get(cv2.CAP_PROP_FPS)}" )
    exit()
else :
    print( "Configuração de câmera OK.")

cv2.namedWindow('preview')

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((pattern_size[1]*pattern_size[0],3), np.float32)
objp[:,:2] = np.mgrid[0:pattern_size[0],0:pattern_size[1]].T.reshape(-1,2)
objp = objp * marker_size

# print('objp:')
# print(objp)

# exit()

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

with np.load(calibration_file) as X:
    mtx, dist = [X[i] for i in ('mtx','dist')]

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if ret :
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            cv2.drawChessboardCorners(frame, pattern_size, corners, ret)
            # print("Corner Points:")
            # corners = corners[[0, 7, -8, -1]].reshape(4, 2)
            # print(corners)
            # break

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

            # print('corners:')
            # print(corners)
            
            # Find the rotation and translation vectors.
            ret,rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

            print(f'Camera position: X:{tvecs[0]}, Y:{tvecs[1]}, and Z:{tvecs[2]}')
            print(f'Camera rotation: X:{rvecs[0]}, Y:{rvecs[1]}, and Z:{rvecs[2]}\n')

            img = draw( frame , corners , imgpts )

            cv2.imshow('preview', img)
        else:
            cv2.imshow('preview', gray)

    else:
        cv2.imshow('preview', gray)

    # Check if the 'q' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
