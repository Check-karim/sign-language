import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

# Initialize the video capture object
cap = cv2.VideoCapture(0)
# Initialize the hand detector
detector = HandDetector(maxHands=1)

offset = 30
imgSize = 300
counter = 0

folder = "data/a"

while True:
    # Read frame from the webcam
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Find hands in the frame
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        # Ensure the cropped image is within bounds
        if imgCropShape[0] > 0 and imgCropShape[1] > 0:
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCalc = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCalc, imgSize))
                wGap = math.ceil((imgSize - wCalc) / 2)
                imgWhite[:, wGap:wCalc + wGap] = imgResize

            else:
                k = imgSize / w
                hCalc = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCalc))
                hGap = math.ceil((imgSize - hCalc) / 2)
                imgWhite[hGap:hCalc + hGap, :] = imgResize

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

    # Display the frame
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
