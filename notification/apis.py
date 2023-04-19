from django.shortcuts import render
from django.http import Http404

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from notification.models import Notification
from notification.serializers import NotificationSerializer


import datetime
from django.utils import timezone
# Create your views here.
            

class NotificationCreateApi(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    

class NotificationListApi(APIView):

    def get(self, request, format=None):
        try:
            time_now = timezone.now()      
            min_date = datetime.datetime(2000,1,1)
            queryset = Notification.objects.filter(issued_date__range=[min_date, time_now]),
            serializer = NotificationSerializer(queryset[0], many=True)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            raise Http404


class NotificationDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'slug'