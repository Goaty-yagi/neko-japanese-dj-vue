from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
from user.models import User
from rest_framework.response import Response
from django.http import HttpResponse

class HttpResponseBadRequest(HttpResponse):
    status_code = 400

class JWTauthentication():
    '''
    Recieve request from middleware. If the request header includes JWT, request.user will be authenticated user  
    '''
    def authenticate(self, request, email=None, password=None, **kwargs):
        auth_data = authentication.get_authorization_header(request)
        print("AUTH",auth_data)
        if not auth_data:
            print("not_auth")
            # request.user will be Anonymous
            return request 
        prefix,decode = auth_data.decode('utf-8').split(' ')
        try:
            # if JWT is invalid or expired, return error
            payload = jwt.decode(decode, settings.JWF_SECRET_KEY, algorithms="HS256")
            print("PL",payload)
            request.user = User.objects.get(UID=payload['user_id'])
            return request
        except jwt.DecodeError as identifier:
            return HttpResponse(identifier, status=500)
            # raise exceptions.AuthenticationFailed(
            #     'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            return HttpResponseBadRequest("you are not allowed to access")
            # raise exceptions.AuthenticationFailed(
            #     'Your token is expired,login')