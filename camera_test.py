
import pyrealsense2 as rs
import numpy as np
import cv2

# Create RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# Enable color and depth
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

print("Starting Intel RealSense camera...")

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # Convert camera image to OpenCV
        image = np.asanyarray(color_frame.get_data())

        # Get distance at center of camera
        x = 320
        y = 240
        distance = depth_frame.get_distance(x, y)

        # Draw center point
        cv2.circle(image, (x, y), 6, (0, 0, 255), -1)

        # Show distance
        cv2.putText(
            image,
            f"Distance: {distance:.3f} m",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.imshow("Intel RealSense Camera", image)

        # ESC to stop
        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()

print("Camera stopped.")

