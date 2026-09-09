

import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        image = np.asanyarray(color_frame.get_data())

        height, width, _ = image.shape

        center_x = width // 2
        center_y = height // 2

        # Distance at camera center
        distance = depth_frame.get_distance(center_x, center_y)

        # Divide screen into LEFT / CENTER / RIGHT
        left_line = width // 3
        right_line = (width * 2) // 3

        cv2.line(image, (left_line, 0), (left_line, height), (255, 255, 255), 2)
        cv2.line(image, (right_line, 0), (right_line, height), (255, 255, 255), 2)

        cv2.putText(
            image,
            "LEFT",
            (60, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            "CENTER",
            (260, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            "RIGHT",
            (500, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.circle(image, (center_x, center_y), 6, (0, 0, 255), -1)

        cv2.putText(
            image,
            f"Center distance: {distance:.2f} m",
            (20, 460),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow("Robot Vision Test", image)

        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
