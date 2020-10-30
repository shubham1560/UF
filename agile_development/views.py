from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .models import Enhancement, Defect
from rest_framework.authtoken.models import Token
# Create your views here.
from .services import add_feature, get_support, get_ticket_detail


class CreateFeatureViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        # breakpoint()
        add_feature(request)
        return Response('', status=status.HTTP_201_CREATED)


class GetSupportRecords(APIView):
    permission_classes = (IsAuthenticated, )

    class FeatureSerializer(serializers.ModelSerializer):
        class Meta:
            model = Enhancement
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on')

    class DefectSerializer(serializers.ModelSerializer):
        class Meta:
            model = Defect
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on')

    def get(self, request, format=None):
        get_support(request)
        d = Defect.objects.filter(sys_created_by=request.user).order_by('-sys_updated_on')
        f = Enhancement.objects.filter(sys_created_by=request.user).order_by('-sys_updated_on')
        defects = self.DefectSerializer(d, many=True)
        features = self.FeatureSerializer(f, many=True)
        return Response({"defects": defects.data, "features": features.data}, status=status.HTTP_200_OK)


class GetSupportRowDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, record_id, record_type, format=None):
        get_ticket_detail(request, record_id, record_type)
        return Response('', status=status.HTTP_200_OK)