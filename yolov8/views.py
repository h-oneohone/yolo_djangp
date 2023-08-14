from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets
from .models import TrafficSign
from .serializers import TrafficSignSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action

from PIL import Image
import numpy as np
import cv2


# Create your views here.
class TrafficSignViewSet(viewsets.ModelViewSet):
    queryset = TrafficSign.objects.all()
    serializer_class = TrafficSignSerializer


class ABCXYZ(viewsets.ModelViewSet):
    queryset = TrafficSign.objects.all()
    serializer_class = TrafficSignSerializer

    

    
class TrafficSignAPIView(APIView):
    def get(self, request, *args, **kwargs):
        traffic_signs = TrafficSign.objects.all()
        serializer = TrafficSignSerializer(traffic_signs,context = {'request':request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)