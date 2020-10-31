from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class CreateHistoryRecord(APIView):

    def post(self, request, format=None):
        pass