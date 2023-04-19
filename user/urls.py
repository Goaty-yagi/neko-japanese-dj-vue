from django.urls import path
from user.apis import (
  UserList, 
  UserDetail, 
  UserAllList, 
  GoogleLogin, 
  UserExist, 
  UserCreation, 
  EmailVerify, 
  Login, 
  SendPasswordChange, 
  PasswordChange, 
  CheckTokenExist, 
  SetTestTakenAndOffset,
  UserDetailPatch, 
  ResendEmailVerification
  )
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
  path('user/', UserList.as_view()),
  # path('csrf/', get_csrf),
  # path('login/', Login.as_view()),
  path('user-list/', UserAllList.as_view()),
  path('user-google/', GoogleLogin.as_view()),
  path('user/<UID>', UserDetail.as_view()),
  path('user-patch/<UID>', UserDetailPatch.as_view()),
  path('user-exists/', UserExist.as_view()),
  path('user-create/', UserCreation.as_view()),
  path('email-verify/', EmailVerify.as_view()),
  path('user-login/', Login.as_view()),
  path('user-send-password-change/', SendPasswordChange.as_view()),
  path('user-password-change/', PasswordChange.as_view()),
  path('token-check/', CheckTokenExist.as_view()),
  path('set-test-taken/', SetTestTakenAndOffset.as_view()),
  path('send-email-verify/', ResendEmailVerification.as_view())
#   path('question/<slug>', ForumQuestionDetail.as_view())
]