from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from knowledge.models import KbKnowledge
from .models import AttachedImage
from rest_framework.views import APIView, status
from rest_framework import serializers
from rest_framework.response import Response
from .services import get_the_link, get_the_url_link_data
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError


class AttachedImageViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if request.user.groups.filter(name="Authors").exists():
            # breakpoint()
            image = request.data["image"]
            if image.size >= 10*1000*1000:
                return Response("Image size more than 10 mb is not allowed!", status=status.HTTP_406_NOT_ACCEPTABLE)
            attachment = AttachedImage()
            attachment.image_caption = request.data['image'].name
            attachment.real_image = image
            attachment.table = "KbKnowledge"
            attachment.sys_created_by = request.user
            attachment.save()
            # up_image = AttachedImage.objects.create(real_image=image)
            response = \
                {"success": 1,
                 "file": {
                     "url": str(attachment.compressed.url)
                 }
                }
        else:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_201_CREATED)


class AttachedImageGenericViewSet(APIView):
    # permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        token = Token.objects.get(key=request.data['token'])
        if token:
            image = request.data["image"]
            if image.size >= 5 * 1000 * 1000:
                return Response("Image size more than 5 mb is not allowed!", status=status.HTTP_406_NOT_ACCEPTABLE)
            attachment = AttachedImage()
            attachment.image_caption = request.data['image'].name
            attachment.real_image = image
            attachment.table = request.data['table']
            attachment.sys_created_by = token.user
            attachment.save()
            response = \
                {"success": 1,
                 "file": {
                     "url": str(attachment.compressed.url),
                     "real_url": str(attachment.real_image.url),
                     "name": attachment.image_caption,
                     "id": attachment.id,
                     "sys_created_on": attachment.sys_created_on
                    }
                }
        else:
            return Response('invalid', status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_201_CREATED)


class AddLinkForVideo(APIView):

    def get(self, request, format=None):
        url = get_the_link(request)
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


class GetAttachment(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = AttachedImage
            fields = ('image_caption', 'compressed', 'real_image_size', 'compressed_image_size', 'sys_created_on')

    def get(self, request, table_name, table_sys_id, format=None):
        print(table_name, table_sys_id)
        if table_name == 'feature':
            table = "Enhancement"
        if table_name == 'defect':
            table = "Defect"
        if request.user.is_staff:
            images = AttachedImage.objects.filter(table=table, table_id=table_sys_id)
        else:
            images = AttachedImage.objects.filter(table=table, table_id=table_sys_id, sys_created_by=request.user)
        result = self.GetUserDetailFromTokenSerializer(images, many=True)
        # breakpoint()
        return Response(result.data, status=status.HTTP_200_OK)