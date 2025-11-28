import cv2
import os
import time

### CHANGE ###
devide_id = 0           # Change the device id
fps = 30.0              # change the fps to match your device
height = 480.0          # change the frame height to match your device
width = 640.0           # change the frame width to match your device
### CHANGE END ###

# Check available formats
# v4l2-ctl -d /dev/video0 --list-formats-ext

cmd = 'v4l2-ctl --set-ctrl=focus_auto=0,white_balance_temperature_auto=0'
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

i = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame in a window
    cv2.imshow('Camera Feed', frame)

    # Check if the 'p' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        # Save the frame as a PNG image
        cv2.imwrite(f'captured_frame_{i}.png', frame)
        i = i + 1
        print(f"Frame saved as 'captured_frame_{i}.png'")

    # Break the loop if the 'q' key is pressed
    elif key == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
