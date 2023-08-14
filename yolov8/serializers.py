from rest_framework import serializers
from .models import TrafficSign

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from PIL import Image
# from ultralytics import YOLO
from io import BytesIO
import onnxruntime as ort
import numpy as np
import cv2
import time
from yolo8.YOLOv8 import YOLOv8


# Load a model
model_path = "models/best.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)


# Hàm chuyển đổi từ OpenCV sang Image
def cv2_to_image(cv2_img):
    # Chuyển mảng ảnh OpenCV thành đối tượng Image
    rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(rgb_img)

    # Tạo tên file tạm thời và định dạng file (có thể sử dụng tên file thật của bạn)
    temp_file_name = "temp_img.jpg"
    temp_file_format = "JPEG"

    # Lưu đối tượng Image thành đối tượng UploadedFile có thể lưu trong Django
    temp_io = BytesIO()
    img_pil.save(temp_io, format=temp_file_format)
    temp_io.seek(0)
    uploaded_image = SimpleUploadedFile(temp_file_name, temp_io.read(), content_type="image/jpeg")

    return uploaded_image


class TrafficSignSerializer(serializers.ModelSerializer):
    name = serializers.CharField( max_length=255)
    image = serializers.ImageField()
    description = serializers.CharField( allow_blank=True)
    class Meta:
        model = TrafficSign
        fields = '__all__'


    def cv2_to_image(self, cv_image):
        # Chuyển đổi từ OpenCV (NumPy array) sang mảng dữ liệu hình ảnh
        pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        return pil_image

    def create(self, validated_data):
        request = self.context.get('request')
        image_file = request.FILES['image']

        # Image.open(image_file).convert('RGB').save(image_file)
        # Read the image data from the file
        image_data = image_file.read()
        
        # Convert image data to a NumPy array
        np_arr = np.frombuffer(image_data, np.uint8)
        
        # Decode the NumPy array into an OpenCV image
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        cv2.imwrite("test.jpg", cv_image)
        # Detect Objects and calculate inference time
        start = time.time()
        boxes, scores, class_ids = yolov8_detector(cv_image)
        end = time.time()
        print("Inference time: ", np.round(end - start, 2), " sec")

        # Draw bounding boxes and labels of detections
        combined_img = yolov8_detector.draw_detections(cv_image)
        cv2.imwrite("test2.jpg", combined_img)
        # Convert to Image object and save to validated_data
        validated_data['image'] = cv2_to_image(combined_img)
        return super().create(validated_data)