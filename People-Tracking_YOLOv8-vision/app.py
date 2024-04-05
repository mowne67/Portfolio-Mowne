import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO  # Assuming you have Ultralytics installed
from collections import defaultdict
import numpy as np
def video_streamer_yolo(video_path, model_path="yolov8n.pt"):
  """ Streams video with YOLOv8 object tracking, saving to a temporary file

  Args:
      video_path: Path to the input video file
      model_path: Path to the YOLOv8 model weights file (default: yolov8n.pt)
  """
  cap = cv2.VideoCapture(video_path)
  track_history = defaultdict(lambda: [])

  # Create temporary file for processed video
  with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
    out_path = temp_file.name

    # Define video writer with desired codec and frame size
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))

    model = YOLO(model_path)  # Load YOLOv8 model

    while True:
      ret, frame = cap.read()
      if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

      # Process frame with YOLOv8
      results = model(frame)

      # Extract detections
      detections = results.xyxy[0]  # Access detections data

      annotated_frame = frame.copy()

      for detection in detections.to_dict("records"):
        x_min, y_min, x_max, y_max, conf, class_id, name = detection.values()
        center_y = (y_min + y_max) / 2

        track = track_history[int(class_id)]  # Track based on class ID
        track.append((float(x_min), float(center_y)))  # Track x, center y

        # Optional: Limit track history length
        # if len(track) > 30:
        #     track.pop(0)

        # Draw bounding box and track line
        cv2.rectangle(annotated_frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 230, 230), thickness=5)

      out.write(annotated_frame)
      cv2.imshow("YOLOv8 Inference", annotated_frame)

      if cv2.waitKey(1) & 0xFF == ord("q"):
          break

    cap.release()
    cv2.destroyAllWindows()

    # Display the temporary video after processing is complete
    st.video(out_path)

# Streamlit App
st.title("YOLOv8 Tracking Streamer")
video_file = st.file_uploader("Upload Video", type=["mp4", "avi"])

if video_file is not None:
  bytes_data = video_file.read()
  video_streamer_yolo(bytes_data)
