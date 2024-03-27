
import cv2
from PIL import Image
import numpy as np

#values for slecting only the blue colour range
lower_blue = np.array([90, 100, 100])
upper_blue = np.array([130, 255, 255])

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsvImage, lower_blue, upper_blue)

    mask1 = Image.fromarray(mask)

    bbox = mask1.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'): #save the image in the boxed region.

        cropped_region = frame[y1:y2, x1:x2]
        cv2.imwrite('cropped_blue_box.jpg', cropped_region)
    
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
