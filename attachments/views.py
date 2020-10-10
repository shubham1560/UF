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
        # breakpoint()
        # url = request.META['QUERY_STRING']
        arr_url_section = request.META['QUERY_STRING'].split('%23')
        arr_url_section[0] = arr_url_section[0].replace("/", "%2F")
        article_id = arr_url_section[0].split('%2F')[-1]
        article = KbKnowledge.objects.get(id=article_id, workflow='published', active=True)
        result = get_the_url_link_data(request, article)
        section = "The whole article has been selected"
        if len(arr_url_section) == 2:
            section = arr_url_section[1]

        response = {
            "success": 1,
            "meta": {
                "result": result,
                "title": article.title,
                "site_name": "Sorted Tree",
                "description": section,
                "image": {
                    "url": url
                }
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class GetEmbedLinkDetail(APIView):
    def get(self, request, format=None):
        # breakpoint()
        url = get_the_link(request)
        result = get_the_url_link_data(request)
        # url = request.META['QUERY_STRING']
        arr_url_section = request.META['QUERY_STRING'].split('%23')
        article_id = arr_url_section[0].split('%2F')[-1]
        article = KbKnowledge.objects.get(id=article_id)
        section = "The whole article has been selected"
        if len(arr_url_section) == 2:
            section = arr_url_section[1]

        response = {
            "success": 1,
            "meta": {
                "result": result,
                "title": article.title,
                "site_name": "Sorted Tree",
                "description": section,
                "image": {
                    "url": url
                }
            }
        }
        return Response(response, status=status.HTTP_200_OK)

