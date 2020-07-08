from .models import SysUser
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response


class GetUserDetailViewSet(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image')

    def get(self, request, format=None):
        # print(request.user.first_name)
        serializer = self.GetUserDetailFromTokenSerializer(request.user, many=False)
        # response = {"user_model": list(request.user.first_name)}
        response = {'user': serializer.data}
        # user = get_user_from_token(token)
        return Response(response, status=status.HTTP_200_OK)