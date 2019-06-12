import numpy as np
import cv2
import datetime
import time
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))
#ret,frame = cap.read()
width, height = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


fps = cap.get(cv2.CAP_PROP_FPS)
print "Fps:",fps


width = int(width)
height = int(height)

print width, height
print 

#width, height, c = frame.shape
#Information to start saving a video
#ret, frame = cap.read()  # import image
#ratio = .5  # resize ratio
#image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # resize image
#width2, height2, channels = image.shape
video = cv2.VideoWriter('RealTime4.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width,height))

framenumber = 0


while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:

        #Time initialization
        t0 = datetime.datetime.now()
        t2 = (t0+ datetime.timedelta(minutes=(1))).strftime("%H:%M:%S")


        #preprocessing
        #frame = cv2.resize(frame, (0,0), None, ratio, ratio)


        median = cv2.medianBlur(frame,5)

        

    

        blur = cv2.GaussianBlur(median,(5,5),0)
    
        fgmask = fgbg.apply(blur)
        kernel = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(fgmask,kernel,iterations = 3)
        #noise removal
        
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_GRADIENT, kernel)
        opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel, iterations = 3)
        

        #human contour detection
        im2, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('Contour',im2)

        print len(contours)

        if len(contours)>10:

        


            cv2.putText(frame, "Frame: " + str(framenumber), (0, 75), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 170, 0), 1)
            cv2.putText(frame, 'Time: ' +str(t2)+ ' sec', (0, 90), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 170, 0), 1)

            video.write(frame)

            cv2.imshow('Record',frame)


        framenumber = framenumber+1

    


        cv2.imshow('frame',fgmask)
        if(cv2.waitKey(30)== ord('q')):
            break
    else:
        break
    
cap.release()

cv2.destroyAllWindows()
