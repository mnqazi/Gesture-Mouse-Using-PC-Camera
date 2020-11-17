
import cv2
#importing numpy for mathematical and matrices
import numpy as np
#importing pyautogui for control mouse and keyboard
import pyautogui

pyautogui.FAILSAFE=False

cap=cv2.VideoCapture(0)
screen_res=pyautogui.size()

#set screen size
cap.set(3,screen_res[0]/2)
cap.set(4,screen_res[1]/2)
video_res=(cap.get(3),cap.get(4))

rx,ry=(2.8,2.9)

ret=True


posXList=list()

posYList=list()

clickHistory=list()

while ret:
    #return frame means return video
    #cap.read means video is read by cap is variable you see in upper
    ret,frame=cap.read()
    flipped=cv2.flip(frame,1)
    #convert Video BGR to HSV
    hsv_frame=cv2.cvtColor(flipped,cv2.COLOR_BGR2HSV)
    #Adding Mask
    mask=cv2.inRange(hsv_frame,np.array([20,130,130]),np.array([30,255,255]))
    # cv2.medianBlur do blured video
    blurred_mask=cv2.medianBlur(mask,5)
    
    k_dilated=np.ones((5,5),np.uint8)
    dilated_mask=cv2.dilate(blurred_mask,k_dilated,5)
    
    
    contours,heirarchy=cv2.findContours(dilated_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #if length of contours greater than 0 then all this thing happened
    if len(contours)>0:
        #M is store all Movement
        M = cv2.moments(contours[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        posX=int(cX*rx)
        posY=int(cY*ry)
        #append position of mouse in posXList
        posXList.append(posX)
        #append position posYList
        posYList.append(posY)

        #length of posXList and posYList
        x_len,y_len=len(posXList),len(posYList)
        #if posY and posX is change then puautogui change the mouse 
        pyautogui.moveTo(posX,posY, duration=0)
        
        if x_len==8:
            print("X list",posXList)
            print("Y list",posYList)
            xmax=max(set(posXList),key=posXList.count)
            ymax=max(set(posYList),key=posYList.count)
            x_count=posXList.count(xmax)
            y_count=posYList.count(ymax)
            if x_count>2 and y_count>2:
        
                if len(clickHistory)==0:
                    clickHistory.append((xmax,ymax))
                    pyautogui.click(x=xmax, y=ymax)
                else:
                    x,y=clickHistory[0]
                    if (xmax in range(x-10,x+10)) and (ymax in range(y-10,y+10)):
                        pyautogui.moveTo(xmax, ymax)
                        pyautogui.click(clicks=2)
                    clickHistory.clear()
                
            posXList.clear()
            posYList.clear()
        
        #circle draw
        cv2.circle(flipped, (cX, cY), 7, (0,255, 0), -1)
        cv2.drawContours(flipped,contours, -1, (0, 0, 255), 2)
    #showing image with imshow on display   
    cv2.imshow("GestureMouseUsingPC-Camera(Developed By Nadeem)",flipped)
    
    #cv2.waitKey is used for quit window
    if cv2.waitKey(1)==27:
        break
#cap.release() means your Camera is closed
cap.release()
#cv2.destroyAllWindows() means quit or close the program if it run after hit on button
cv2.destroyAllWindows()
