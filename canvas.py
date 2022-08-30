import cv2
import mediapipe as mp
import time
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)
imgCanvas = np.zeros((480,720,3),np.uint8)
imgCanvas.fill(255)
mphands = mp.solutions.hands
hands = mphands.Hands(min_detection_confidence=0.6)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
tipID = [4,8,12,16,20]
while True:
   success, img = cap.read()
   img = cv2.flip(img,1)
   imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
   result = hands.process(imgRGB)
   if result.multi_hand_landmarks:
       lmlist = []
       for handlm in result.multi_hand_landmarks:
           for id, lm in enumerate(handlm.landmark):
               h, w, c = img.shape
               cx , cy = int(lm.x*w), int(lm.y*h)
               lmlist.append([id,cx,cy])
               if len(lmlist) == 21:
                   xp,yp = 0, 0
                   # tip of index finger
                   x1,y1 = lmlist[8][1:]
                   # tip of middle finger
                   x2, y2 = lmlist[12][1:]

                   count = []

                    # Counting LEFT HAND Thumb
                   if lmlist[4][1] < lmlist[3][1]:
                       count.append(1)

                   else:
                       count.append(0)
                   for id in range(1, 5):
                        #counting fingers
                       if lmlist[tipID[id]][2] < lmlist[tipID[id] - 2][2]:
                           count.append(1)
                       else:
                           count.append(0)
                    # Eraser Mode, only erase with two finger
                   if count[1] and count[2]:
                       cv2.rectangle(img, (x1, y1-25), (x2,y2+25), (255,255,255), cv2.FILLED)
                       if xp == 0 and yp == 0:
                           xp, yp = x1, y1
                       cv2.rectangle(imgCanvas, (x1, y1-25), (x2,y2+25), (255,255,255), cv2.FILLED)
                       xp, yp = x1, y1

                       print("select")
                    # Drawing Mode, only draw with index finger
                   if count[1] and count[2]== False:
                       draw = (255,0,0)
                       cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                       if xp == 0 and yp== 0:
                           xp,yp = x1,y1
                       cv2.line(img, (xp, yp), (x1, y1), (255, 0, 0), 15)
                       cv2.line(imgCanvas, (xp, yp), (x1, y1),(255,0,0), 15)
                       xp,yp = x1,y1
                       print("edit")






           mpDraw.draw_landmarks(img,handlm, mphands.HAND_CONNECTIONS)
   cTime = time.time()
   fps = 1/(cTime-pTime)
   pTime = cTime
   # printing fps
   cv2.putText(img,f'FPS: {int(fps)}',(10,50), cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)

   cv2.imshow("Input", img)
   cv2.imshow("Output",imgCanvas)
   if cv2.waitKey(1) & 0xFF == ord('q'):
     break

