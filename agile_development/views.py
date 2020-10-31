from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .models import Enhancement, Defect
from .services import add_feature, get_support, get_ticket_detail


class CreateFeatureViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        # breakpoint()
        id = add_feature(request)
        return Response(id, status=status.HTTP_201_CREATED)


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

    class FeatureStaffSerializer(serializers.ModelSerializer):
        class Meta:
            model = Enhancement
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on', 'get_created_by')

    class DefectStaffSerializer(serializers.ModelSerializer):
        class Meta:
            model = Defect
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on', 'get_created_by')

    def get(self, request, format=None):
        get_support(request)
        if request.user.is_staff:
            d = Defect.objects.all().order_by('-sys_updated_on')
            f = Enhancement.objects.all().order_by('-sys_updated_on')
            defects = self.DefectStaffSerializer(d, many=True)
            features = self.FeatureStaffSerializer(f, many=True)
        else:
            d = Defect.objects.filter(sys_created_by=request.user).order_by('-sys_updated_on')
            f = Enhancement.objects.filter(sys_created_by=request.user).order_by('-sys_updated_on')
            defects = self.DefectSerializer(d, many=True)
            features = self.FeatureSerializer(f, many=True)
        return Response({"defects": defects.data, "features": features.data}, status=status.HTTP_200_OK)


class GetSupportRowDetail(APIView):
    permission_classes = (IsAuthenticated, )

    class FeatureSerializer(serializers.ModelSerializer):
        class Meta:
            model = Enhancement
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on',
                      'sys_updated_on', 'work_notes', 'additional_comments', 'priority')

    class FeatureStaffSerializer(serializers.ModelSerializer):
        class Meta:
            model = Enhancement
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on',
                      'sys_updated_on', 'work_notes', 'additional_comments', 'priority', 'get_created_by')

    class DefectStaffSerializer(serializers.ModelSerializer):
        class Meta:
            model = Defect
            fields = ('id', 'short_description', 'description', 'state', 'sys_created_on',
                      'sys_updated_on', 'work_notes', 'additional_comments', 'priority', 'get_created_by')

    def get(self, request, record_id, record_type, format=None):
        result = ''
        if record_type == 'defect':
            # support
            if request.user.is_staff:
                try:
                    support = Defect.objects.get(id=record_id)
                    result = self.DefectStaffSerializer(support, many=False)
                except ObjectDoesNotExist:
                    pass

            else:
                try:
                    support = Defect.objects.get(id=record_id, sys_created_by=request.user)
                    result = self.DefectSerializer(support, many=False)
                except ObjectDoesNotExist:
                    pass
        if record_type == 'feature':
            if request.user.is_staff:
                try:
                    support = Enhancement.objects.get(id=record_id)
                    result = self.FeatureStaffSerializer(support, many=False)
                except ObjectDoesNotExist:
                    pass
            else:
                try:
                    support = Enhancement.objects.get(id=record_id, sys_created_by=request.user)
                    result = self.FeatureSerializer(support, many=False)
                except ObjectDoesNotExist:
                    pass
        if result == '':
            return Response('', status=status.HTTP_404_NOT_FOUND)
        return Response(result.data, status=status.HTTP_200_OK)