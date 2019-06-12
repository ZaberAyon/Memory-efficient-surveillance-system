import numpy as np
import cv2
cap = cv2.VideoCapture("night.MKV")
fgbg = cv2.createBackgroundSubtractorMOG2()

#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))
ret,frame = cap.read()
frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)



width = int(width)
height = int(height)

print width, height
 

#width, height, c = frame.shape
#Information to start saving a video
ret, frame = cap.read()  # import image
ratio = .5  # resize ratio
image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # resize image
width2, height2, channels = image.shape
video = cv2.VideoWriter('Output_5.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (height2,width2),1)

framenumber = 0


while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:

        #resize frame
        frame = cv2.resize(frame, (0,0), None, ratio, ratio)


        #preprocessing
        


        median = cv2.medianBlur(frame,5)

        area =0

        

    

        blur = cv2.GaussianBlur(median,(5,5),0)
    
        fgmask = fgbg.apply(blur)
        cv2.imshow("Foreground Mask",fgmask)
        #Shadow Removal
        
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        
        kernel = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(imBin,kernel,iterations = 3)
        #noise removal
        
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_GRADIENT, kernel)
        opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel, iterations = 3)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations = 3)

        cv2.imshow("Closing",closing)

        #human contour detection
        im2, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('Contour',im2)

        #for i in contours:
            #area1 = cv2.contourArea(i)
            #area = area1+area
            #print area

        print len(contours)
        

        if len(contours)>5:

        


            cv2.putText(frame, "Frame: " + str(framenumber) + ' of ' + str(frames_count), (0, 75), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 170, 0), 1)
            cv2.putText(frame, 'Time: ' + str(round(framenumber / fps, 2)) + ' sec of ' + str(round(frames_count / fps, 2))
                    + ' sec', (0, 90), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 170, 0), 1)

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
