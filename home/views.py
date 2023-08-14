from django.shortcuts import render
from django.http import HttpResponse
from .forms import UpLoadImgForm
from .models import UpLoadImg

import numpy as np
from ultralytics import YOLO
import cv2
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

# Load a model
model = YOLO(r"C:\Users\Lenovo\Desktop\hung\yolov8\best.pt")  # load a pretrained model

# Hàm chuyển đổi từ OpenCV sang Image
def cv2_to_image(cv2_img):
    # Chuyển mảng ảnh OpenCV thành đối tượng Image
    img_pil = Image.fromarray(cv2_img)

    # Tạo tên file tạm thời và định dạng file (có thể sử dụng tên file thật của bạn)
    temp_file_name = "temp_img.jpg"
    temp_file_format = "JPEG"

    # Lưu đối tượng Image thành đối tượng UploadedFile có thể lưu trong Django
    temp_io = BytesIO()
    img_pil.save(temp_io, format=temp_file_format)
    temp_io.seek(0)
    uploaded_image = SimpleUploadedFile(temp_file_name, temp_io.read(), content_type="image/jpeg")

    return uploaded_image
# Create your views here.
def index(request):
    UF = UpLoadImgForm()
    return render(request, 'index.html', {'UF':UF})

# Upload image
def upload(request):
    if request.method == 'POST':
        UF = UpLoadImgForm(request.POST, request.FILES)
        if UF.is_valid():
            img_instance = UF.save()

            # Đọc ảnh từ đối tượng UploadedFile và chuyển về định dạng OpenCV
            img_file = img_instance.img  
            img_data = img_file.read()
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            img_cv = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)

            # Áp dụng YOLO để nhận diện
            results = model(img_cv)

            # Chuyển kết quả về đối tượng Image và lưu lại
            res = results[0].plot()
            img_instance.img = cv2_to_image(res)
            img_instance.save()
            return HttpResponse('Upload Success!')
        else:
            return HttpResponse('Upload Fail!')
    else:
        return HttpResponse('not POST')