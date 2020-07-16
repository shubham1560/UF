from .models import SysUser
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
# from .services import remove_user
from rest_framework.authtoken.models import Token


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
        user.profile = request.data['profile']
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
        user.profile = request.data['profile']
        user.save()
        return Response({"message": "changed the image mofo"}, status=status.HTTP_200_OK)
