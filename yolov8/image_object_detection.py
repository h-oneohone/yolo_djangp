import cv2
from imread_from_url import imread_from_url
from PIL import Image
from yolo8 import YOLOv8
import time
import numpy as np

# Initialize yolov8 object detector
model_path = "models/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)

# # Read image
# img_url = "00022_jpg.rf.b8f5642bbdc6513630cdd88e37ccbf90.jpg"
# img = imread_from_url(img_url)

# Read image from path
img_path = "00022_jpg.rf.b8f5642bbdc6513630cdd88e37ccbf90.jpg"
img = cv2.imread(img_path)

# Detect Objects
start = time.time()
boxes, scores, class_ids = yolov8_detector(img)
end = time.time()
print("Inference time: ", np.round(end - start, 2), " sec")

# Draw detections
combined_img = yolov8_detector.draw_detections(img)
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
cv2.imshow("Detected Objects", combined_img)

cv2.waitKey(0)
