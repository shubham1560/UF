from .models import SysUser
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
# from .services import remove_user


class GetUserDetailViewSet(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image')

    def get(self, request, format=None):
        # breakpoint()
        # print(reques  t.user.first_name)
        if request.data["delete"]:
            # remove_user(request.user)
            request.user.delete()
            response = {"message": "User Deleted Successfully"}
            return Response(response, status=status.HTTP_200_OK)

        serializer = self.GetUserDetailFromTokenSerializer(request.user, many=False)
        # response = {"user_model": list(request.user.first_name)}
        response = {'user': serializer.data}
        # user = get_user_from_token(token)
        return Response(response, status=status.HTTP_200_OK)

