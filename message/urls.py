from django.urls import path
from message.views import SendVerificationEmail
from allauth.account.views import EmailView

urlpatterns = [
  path('send-verification-email/', SendVerificationEmail.as_view()),
]