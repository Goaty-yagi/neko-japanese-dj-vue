from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.response import Response
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
import os

# from user.authentications import JWTauthentication
from allauth.account.models import EmailAddress

class HttpResponseBadRequest(JsonResponse):
    status_code = 400

class AccessRestrictMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        print("ARM")
        if "quiz_api.settings.local" != os.environ['DJANGO_SETTINGS_MODULE']:
            if "HTTP_ORIGIN" in request.META:
                return self.get_response(request)

            if "HTTP_REFERER" in request.META:
                if "admin" in request.META["HTTP_REFERER"]:
                    print("from_admin")
                    return self.get_response(request)
                else:
                    print("404")
                    return HttpResponseBadRequest("you are not allowed to access")
            else:
                print(request.META["PATH_INFO"])
                if "/admin" in request.META["PATH_INFO"]:
                    print("PATHINFO")
                    return self.get_response(request)
                else:
                    print("ELSE")
                    import environ
                    env = environ.Env()
                    url = os.environ['FRONT_ORIGIN']
                    return redirect(url)
        else:
            return self.get_response(request)



from user.models import User
from rest_framework import authentication
import jwt

class JWTAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        '''
        Recieve request from middleware. If the request header includes JWT, request.user will be authenticated user  
        '''
        
        auth_data = authentication.get_authorization_header(request)
        print("AUTH_DATA",request.headers)
        # if "credentials" in request:
        #     print("AUTH",request.credentials)
        if not auth_data:
            print("not_auth", request.user)
            # request.user will be Anonymous
            return self.get_response(request) 
        prefix,decode = auth_data.decode('utf-8').split(' ')
        try:
            # if JWT is invalid or expired, return error
            payload = jwt.decode(decode, settings.JWF_SECRET_KEY, algorithms="HS256")
            print("PL",payload)
            request.user = User.objects.get(UID=payload['user_id'])
            print(request.user)
            # authenticate()
            return self.get_response(request)
        except jwt.DecodeError as identifier:
            # return HttpResponse(identifier, status=500)
            return HttpResponseBadRequest({"message":'Your token is invalid', "token_not_pass":True})
            # raise exceptions.AuthenticationFailed(
            #     'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            return HttpResponseBadRequest({"message":'Your token is expired', "token_not_pass":True})
            # raise exceptions.AuthenticationFailed(
        #     'Your token is expired,login')