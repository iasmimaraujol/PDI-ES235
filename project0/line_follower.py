import cv2
import numpy as np
import time

try:
    import sim
except:
    print('"sim.py" could not be imported. Check whether "sim.py" or the remoteApi library could not be found. '
          'Make sure both are in the same folder as this file')

def load_image(image, resolution):
    return cv2.flip(np.array(image, dtype=np.uint8).reshape((resolution[1], resolution[0], 3)), 0)




def main():
    lm = 1
    rm = -1
    a = 0
    d = 0

    print('Program Started')
    sim.simxFinish(-1) # just in case, close all opened connections
    # establishes a connection between python and coppelia
    clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    if clientID != -1:
        print('Connected to remote API server')
    else:
        print('Failed connecting to remote API server')

    return_code, camera = sim.simxGetObjectHandle(clientID, "kinect_rgb",
                                                  sim.simx_opmode_oneshot_wait)
    return_code, left_motor = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor",
                                                      sim.simx_opmode_oneshot_wait)
    return_code, right_motor = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor",
                                                       sim.simx_opmode_oneshot_wait)
    return_code, pioneer = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx",
                                                   sim.simx_opmode_oneshot_wait)
    
    sim.simxSetJointTargetVelocity(clientID, left_motor, 0, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID, right_motor, 0, sim.simx_opmode_streaming)

    return_code, _, _ = sim.simxGetVisionSensorImage(clientID, camera, 0, sim.simx_opmode_streaming)
    return_code, position = sim.simxGetObjectPosition(clientID, pioneer, -1,  sim.simx_opmode_streaming)
    time.sleep(0.5)


    while clientID != -1:
        return_code, resolution, image = sim.simxGetVisionSensorImage(clientID, camera, 0,
                                                                      sim.simx_opmode_buffer)
        if return_code == sim.simx_return_ok:
            # Load image
            imagem = load_image(image, resolution)
            ##########

            # find row, colum and chanel in the image
            (row, colum, chanels) = imagem.shape

            # transformando parea escala de cinza
            gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

            # binario
            ret, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

            for r in range(row):
                if (img[400][r] == 0):
                    a = a + r
                    d = d + 1

            if a > 0:
                tt = a/d - 320
                a = 0
                d = 0

                if tt < 0:
                    lm =  0.4
                    rm =  1.8
         
                if tt > 0:
                    tt = np.abs(tt)
                    rm =  0.4
                    lm =  1.8




            ##########
            sim.simxSetJointTargetVelocity(clientID, left_motor, lm, sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(clientID, right_motor, rm, sim.simx_opmode_streaming)


    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)

    # Stop simulation
    sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot_wait)

if __name__ == '__main__':
    main()