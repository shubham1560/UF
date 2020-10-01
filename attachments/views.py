from django.shortcuts import render
from .models import AttachedImage
from rest_framework.views import APIView, status
from rest_framework.response import Response


class AttachedImageViewSet(APIView):

    def post(self, request, format=None):
        # breakpoint()
        image = request.data["image"]
        attachment = AttachedImage()
        attachment.real_image = image
        attachment.save()
        # up_image = AttachedImage.objects.create(real_image=image)
        response = \
            {"success": 1,
             "file": {
                "url": str(attachment.compressed.url)
                }
            }
        # response = {"image_url": str(attachment.real_image.url), "compressed_image_url": str(attachment.compressed.url)}
        # response = {"message": "image uploaded"}
        return Response(response, status=status.HTTP_201_CREATED)



