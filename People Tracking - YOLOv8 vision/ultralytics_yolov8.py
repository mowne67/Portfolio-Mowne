import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
import tempfile
model = YOLO('yolov8n.pt')

video_path = "videos/store.mp4"
cap = cv2.VideoCapture(video_path)
track_history = defaultdict(lambda: [])
while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.track(source=frame, persist=True)

        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        annotated_frame = results[0].plot()
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y+h/2)))  # x, y center point
            # if len(track) > 30:  # retain 90 tracks for 90 frames
            #     track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 230, 230), thickness=5)

        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


