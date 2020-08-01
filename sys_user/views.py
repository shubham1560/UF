from .models import SysUser
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from .services import get_user_activity
from rest_framework.authtoken.models import Token
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def compressImage(uploadedImage):
    imageTemproary = Image.open(uploadedImage).convert('RGB')
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((200, 200))
    imageTemproaryResized.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


class GetUserDetailViewSet(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image', 'email',
                      'about', 'header_image')

    def get(self, request, format=None):
        serializer = self.GetUserDetailFromTokenSerializer(request.user, many=False)
        response = {'user': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.data["delete"]:
            request.user.delete()
            response = {"message": "User Deleted Successfully"}
            return Response(response, status=status.HTTP_200_OK)


class EditUserDetailViewSet(APIView):

    def post(self, request, format=None):
        # breakpoint()
        user = request.user
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        # user.profile = request.data['profile']
        user.about = request.data['about']
        user.save()
        return Response({"message": "changed"}, status=status.HTTP_200_OK)


class EditImageOnlyViewSet(APIView):
    class EditImageOnlySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = SysUser
            fields = ['profile']

    def post(self, request, format=None):
        # breakpoint()
        user = Token.objects.get(key=request.data['token']).user
        user.profile = compressImage(request.data['profile'])
        user.save()
        return Response({"message": "changed the image mofo"}, status=status.HTTP_200_OK)


class GetUserActivity(APIView):

    def get(self, request, requested_type, format=None):
        result = get_user_activity(request, requested_type)
        # breakpoint()
        return Response(result, status=status.HTTP_200_OK)
