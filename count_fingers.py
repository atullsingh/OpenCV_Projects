import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
tipID = [4,8,12,16,20]
while True:
   success, img = cap.read()
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


                   print(count)
                   total = count.count(1)
                   # showing counted fingers
                   cv2.putText(img, str(total), (500, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 6)



           mpDraw.draw_landmarks(img,handlm, mphands.HAND_CONNECTIONS)
   cTime = time.time()
   fps = 1/(cTime-pTime)
   pTime = cTime
   # printing fps
   cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
   cv2.imshow("Video",img)
   if cv2.waitKey(1) & 0xFF == ord('q'):
     break

