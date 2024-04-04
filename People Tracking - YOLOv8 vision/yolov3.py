import cv2
import numpy as np

# Load YOLO pre-trained model
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")

# Load COCO class names (coco.names file)
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Set input video file
#video_path = "path/to/your/video.mp4"
cap = cv2.VideoCapture("videos/store.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Create blob from frame
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)

    # Set input blob to the network
    net.setInput(blob)

    # Get output layer names
    output_layers = net.getUnconnectedOutLayersNames()

    # Forward pass through the network
    detections = net.forward(output_layers)

    # Process detections
    for detection in detections:
        # Extract class ID, confidence, and bounding box coordinates
        for obj in detection:
            scores = obj[5:]
            class_id = scores.argmax()
            confidence = scores[class_id]

            if confidence > 0.3:
                # Object detected
                label = classes[class_id]
                box = obj[0:4] * np.array([width, height, width, height])
                x, y, w, h = box.astype(int)

                # Draw bounding box and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

