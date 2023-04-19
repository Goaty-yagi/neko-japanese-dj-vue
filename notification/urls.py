from django.urls import path, include
from notification.apis import NotificationCreateApi, NotificationListApi, NotificationDetailApi

urlpatterns = [
  path('notification/create', NotificationCreateApi.as_view()),
  path('notification/list', NotificationListApi.as_view()),
  path('notification/detail/<slug>', NotificationDetailApi.as_view()),
]