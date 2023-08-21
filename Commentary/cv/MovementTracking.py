import cv2
import mediapipe as mp
import time
import math
import numpy as np
import json
import os
import glob

i = 1

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        # self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
        #                              self.detectionCon, self.trackCon)
        self.pose = self.mpPose.Pose()
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        # print(angle)
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

def process_image(detector, img, current_y, prev_y, last_fall_time):

    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        current_y = lmList[24][2]
        cv2.circle(img, (lmList[24][1], lmList[24][2]), 15, (0, 0, 255), cv2.FILLED)

        # if prev_y and current_y - prev_y > 20:
        #     print("Fall Difference:", prev_y and current_y - prev_y)
        #     if time.time() - last_fall_time > 2:
        #         print("**************************")
        #         print("*     Fall Detected!     *")
        #         print("**************************")
        #         last_fall_time = time.time()

        prev_y = current_y
    
    path_to_file = "/Users/tonsonwang/Desktop/Commentary/express_server/boundingBox.txt"
    with open(path_to_file, "r") as file:
        for line in file:
            coordinates = json.loads(line.strip())
            startX = coordinates["startX"]
            startY = coordinates["startY"]
            x = coordinates["x"]
            y = coordinates["y"]
            isFinish = coordinates["finish"]

            if isFinish:
                cv2.rectangle(img, (startX, startY), (x, y), (255, 255, 0), 2)
                if len(lmList) != 0:
                    left_hand_x = lmList[19][1]
                    left_hand_y = lmList[19][2]
                    right_hand_x = lmList[20][1]
                    right_hand_y = lmList[20][2]
                    if startX <= left_hand_x <= x and startY <= left_hand_y <= y:
                        print("Left hand is inside the bounding box")
                        cv2.circle(img, (1, 1), radius=5, color=(0, 0, 255), thickness=-1)
                        timestamp = str(time.time()).replace('.', '_')
                        output_path = os.path.join('FinishImg', 'processed_' + timestamp + '.jpg')
                        cv2.imwrite(output_path, img)
                    else:
                        # print("Left hand is outside the bounding box")
                        cv2.circle(img, (1, 1), radius=5, color=(0, 0, 255), thickness=-1)

                    if startX <= right_hand_x <= x and startY <= right_hand_y <= y:
                        
                        print("Right hand is inside the bounding box")
                        cv2.circle(img, (1, 1), radius=5, color=(0, 0, 255), thickness=-1)
                        timestamp = str(time.time()).replace('.', '_')
                        output_path = os.path.join('FinishImg', 'processed_' + timestamp + '.jpg')
                        cv2.imwrite(output_path, img)
                    else:
                        # print("Right hand is outside the bounding box")
                        cv2.circle(img, (1, 1), radius=5, color=(0, 0, 255), thickness=-1)

            else:
                cv2.rectangle(img, (startX, startY), (x, y), (0, 255, 0), 2)

    return img, prev_y, last_fall_time

def display_frame(img, fps):
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)


# def main():
#     cap = cv2.VideoCapture('PoseVideos/1.mp4')
#     pTime = 0
#     detector = poseDetector()
#     prev_y = None
#     last_fall_time = 0
#     first_frame = True
#     boxes = []

#     while True:
#         success, img = cap.read()
#         cTime = time.time()

#         if cTime != pTime:
#             img, prev_y, last_fall_time = process_image(detector, img, prev_y, prev_y, last_fall_time)
#             fps = 1 / (cTime - pTime)
#             pTime = cTime

#             display_frame(img, fps)


# if __name__ == "__main__":
#     main()


# def main():
#     input_folder = '/Users/tonsonwang/Desktop/expressServer/frames'  # Folder to read images from
#     output_folder = 'ProcessedImg'  # Folder to save processed images

#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     pTime = 0
#     detector = poseDetector()
#     prev_y = None
#     last_fall_time = 0

#     processed_files = set()  # Keep track of files already processed

#     while True:
#         for filename in os.listdir(input_folder):
#             if filename in processed_files:  # Skip if already processed
#                 continue

#             img_path = os.path.join(input_folder, filename)
#             img = cv2.imread(img_path)
#             if img is None:
#                 print(f"Error loading image {img_path}")
#                 continue

#             height, width, _ = img.shape
#             print(height)
#             print(width)

#             img_copy = img.copy()
#             cTime = time.time()
#             img_copy, prev_y, last_fall_time = process_image(detector, img_copy, prev_y, prev_y, last_fall_time)
#             fps = 1 / (cTime - pTime)
#             pTime = cTime

#             # Saving the processed image
#             output_path = os.path.join(output_folder, 'processed_' + filename)
#             cv2.imwrite(output_path, img_copy)
#             print(f"Image saved to {output_path}")

#             processed_files.add(filename)  # Mark as processed

#         time.sleep(1)  # Wait for a second before checking the folder again

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


def main():
    deleteProcessedImg = True

    if deleteProcessedImg:
        processed_img_folder = 'ProcessedImg'
        files = glob.glob(os.path.join(processed_img_folder, '*.jpg'))
        for f in files:
            os.remove(f)
        processed_img_folder = 'FinishImg'
        files = glob.glob(os.path.join(processed_img_folder, '*.jpg'))
        for f in files:
            os.remove(f)

    input_folder = '/Users/tonsonwang/Desktop/Commentary/express_server/frames'
    output_folder = 'ProcessedImg'
    

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pTime = 0
    detector = poseDetector()
    prev_y = None
    last_fall_time = 0

    processed_files = set()

    while True:
        for filename in os.listdir(input_folder):
            if filename in processed_files:  # Skip if already processed
                continue

            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Waiting to start...")
                continue

            height, width, _ = img.shape


            img_copy = img.copy()
            cTime = time.time()
            img_copy, prev_y, last_fall_time = process_image(detector, img_copy, prev_y, prev_y, last_fall_time)
            fps = 1 / (cTime - pTime)
            pTime = cTime

            output_path = os.path.join(output_folder, 'processed_' + filename)
            cv2.imwrite(output_path, img_copy)
            print(f"Image saved to {output_path}")

            processed_files.add(filename)

        time.sleep(1)  

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
