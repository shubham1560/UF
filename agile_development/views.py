from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.
from .services import add_feature


class CreateFeatureViewSet(APIView):
    # permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        # breakpoint()
        add_feature(request)
        return Response('', status=status.HTTP_201_CREATED)