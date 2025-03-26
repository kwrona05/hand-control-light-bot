import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Start video capture
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break  # Exit loop if frame not captured

    frame = cv2.flip(frame, 1)  # Flip for a mirror effect
    hands, img = detector.findHands(frame, flipType=False)  # Detect hands

    if hands:
        lmList = hands[0]['lmList']
        fingerUp = detector.fingersUp(hands[0])

        print(fingerUp)  # Debugging output
        cnt.leds_control(fingerUp)  # Send finger state to controller

        # Finger count mapping
        finger_count = sum(fingerUp)
        cv2.putText(frame, f'Finger count: {finger_count}', (20, 460),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # Display frame
    cv2.imshow("frame", frame)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
