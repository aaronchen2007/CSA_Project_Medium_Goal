import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("/Users/aaronchen/Documents/GitHub/CSA_Project_Medium_Goal/AI Trainer/Kettlebell Curls.mp4")

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    # img = cv2.imread("/Users/aaronchen/Documents/GitHub/CSA_Project_Medium_Goal/AI Trainer/Kettlebell Curls.jpeg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    # Right Arm
    if len(lmList) != 0:
        angle = detector.findAngle(img, 12, 14, 16, text=False)
        per = np.interp(angle, (50,150),(0,100))
        bar = np.interp(angle, (220, 310), (650, 100))

        print(angle,per)

        # Check for the curls
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), thickness=4)

        cv2.rectangle(img, (0,450), (250,720), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45,670), cv2.FONT_HERSHEY_PLAIN, 15, (255,0,0), thickness=25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
