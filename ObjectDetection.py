import depthai as dai   # Luxonis Camera library
import serial           # Serial port library
import cv2              # OpenCV library
import numpy as np
import time

# Connect to Arduino
arduino = serial.Serial('/dev/tty.usbmodem14101', 9600)  # Update as needed

# Setup OAK-1 pipeline
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setPreviewSize(640, 480)
cam.setInterleaved(False)
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)

with dai.Device(pipeline) as device:
    queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    last_angle = None
    last_sent_time = 0
    cooldown_ms = 750  # Minimum time between servo updates in milliseconds

    # This will run till script is manually stopped
    while True:
        frame = queue.get().getCvFrame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, (0,120,70), (10,255,255))
        mask2 = cv2.inRange(hsv, (170,120,70), (180,255,255))
        mask = mask1 | mask2

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Contour was detected
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cx = x + w // 2

            # Draw rectangle around the object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Map position to 0–180 degrees (reversed)
            angle = 180 - int((cx / 640) * 180)

            # Added a slight delay to avoid angle flickering between single degree angles
            current_time = time.time() * 1000
            if (current_time - last_sent_time) > cooldown_ms:
                arduino.write(f"X{angle}\n".encode())
                last_angle = angle
                last_sent_time = current_time

            # Display current angle
            cv2.putText(frame, f"Angle: {angle}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 0), 2)
        else:
            cv2.putText(frame, "No red object found", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Vision Based Object Tracking System", frame)
        if cv2.waitKey(1) == ord('q'):
            break
