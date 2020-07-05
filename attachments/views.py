from django.shortcuts import render
from .models import AttachedImage
# from rest_framework.views import APIView,
from rest_framework import viewsets
from rest_framework import serializers
from django.http import HttpResponse


# Create your views here.
class AttachedImageViewSet(viewsets.ModelViewSet):
    class AttachedImageSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = AttachedImage
            fields = ['id', 'article', 'real_image']

    queryset = AttachedImage.objects.all()
    serializers = AttachedImageSerializer

    class AttachedImageSerializer(serializers.ModelSerializer):

        class Meta:
            model = AttachedImage
            fields = ('id', 'real_image', 'article')

    def post(self, request, format=None):
        image = request.data["image"]
        upImage = AttachedImage.objects.create(real_image=image)
        return HttpResponse({"message": upImage.real_image})


