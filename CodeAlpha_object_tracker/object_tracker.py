import cv2
from ultralytics import YOLO

def run_object_tracking(video_source, output_name="tracked_output.mp4"):
    # 1. LOAD PRETRAINED YOLO MODEL
    # 'yolov8n.pt' or 'yolo11n.pt' are nano models that download automatically on first run
    print("Initializing YOLO framework...")
    model = YOLO("yolov8n.pt") 

    # 2. SETUP VIDEO STREAM ENTRY
    # Pass 0 instead of a file path if you want to use your laptop webcam!
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source '{video_source}'")
        return

    # Get video properties for output formatting
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0: fps = 30 # Fallback default if stream reading fails

    # Configure VideoWriter to output tracking result to a playable file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_name, fourcc, fps, (frame_width, frame_height))

    print(f"Processing frames. Press 'q' inside the video window to quit early...")

    # 3. INTERATE OVER SENSORY VIDEO FRAMES
    while cap.isOpened():
        success, frame = cap.read()
        
        if not success:
            print("Video stream finished or frame processing interrupted.")
            break

        # Run multi-object tracking with standard persistence between frames
        # persist=True ensures object IDs are assigned smoothly across time indexes
        results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)

        # Plot the visual tracked bounding boxes directly back onto the frame matrix
        annotated_frame = results[0].plot()

        # Write out the frame to the saved compilation path
        out.write(annotated_frame)
        cv2.imshow("Ultralytics YOLO Real-Time Tracker", annotated_frame)

        # Early termination trigger by hitting the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Tracking session canceled manually by user request.")
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Tracking completely compiled! File saved as: {output_name}")

if __name__ == "__main__":
    # Sample download link or placeholder string. 
    # Replace this string with a path to your own video file (e.g., "cars_driving.mp4")
    # OR change it to 0 to test it instantly with your live Webcam feed!
    video_path = 0
    
    run_object_tracking(video_path)
