from django.shortcuts import render

from knowledge.models import KbKnowledge
from .models import AttachedImage
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .services import get_the_link, get_the_url_link_data


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


class AddLinkForVideo(APIView):

    def get(self, request, format=None):
        # breakpoint()
        url = get_the_link(request)
        result = get_the_url_link_data(request)
        # url = request.META['QUERY_STRING']

        response = {
            "success": 1,
            "meta": {
                "result": result,
                "title": "CodeX Team",
                "site_name": "CodeX",
                "description": "Club of web-development, design and marketing. We build team learning how to build full-valued projects on the world market.",
                "image": {
                    "url": url
                }
            }
        }
        return Response(response, status=status.HTTP_200_OK)

