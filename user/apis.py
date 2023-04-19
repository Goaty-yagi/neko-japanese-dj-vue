from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

from django.http import Http404
from django.shortcuts import get_object_or_404

from django.db.models import Prefetch
from django.http import QueryDict
import uuid

import copy
# from ipware import get_client_ip

from user.models import User
from django.contrib.auth.models import User as AuthUser
from board.models import BoardQuestion, BoardAnswer
from user.serializers import UserSerializer,UserStrageSerializer, SimpleUserSerializer, UserCreateSerializer
from quiz.models import UserStatus, QuizTaker, ParentStatus, ParentQuiz
from quiz.serializers import UserStatusSerializer,QuizTakerSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.authtoken.models import Token

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.utils import JWTCookieAuthentication
from dj_rest_auth.jwt_auth import JWTCookieAuthentication as J
from rest_framework.permissions import IsAuthenticated, AllowAny
from dj_rest_auth.views import LoginView

from django.contrib.auth import authenticate, login
from .messages.email_varifications import SendVerificationEmail, SendPasswordReset

from io import BytesIO
from PIL import Image
from django.core.files import File


# print(JWTCookieAuthentication.__getattribute__("koko","set"))

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # serializer_class = GoogleRegisterSerializer
    
class Login(APIView):
    permission_classes = ([AllowAny])
    def post(self, request, format=None):
        print("LOGIN",self.__dir__())
        print("REQUEST",request.__dir__(), request.data, )
        username = request.data["username"]
        email = email = request.data["email"]
        user = authenticate(username=username ,email = email)
        print("user", user)
        # user = User.objects.get(email = request.data["email"])
        a = login(request, user)
        print("A",a)

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }

class UserCreation(APIView):
    permission_classes = ([AllowAny])

    def post(slef, request, format=None):
        user = User.objects.create_user(**request.data)
        user.is_active = False
        print('GONNA SAVE')
        user.save()
        # serializer = UserCreateSerializer(data=user)
        # if serializer.is_valid():
        # token = get_tokens_for_user(user)
        # request = {
        #     "email":user.email,
        #     "access_token":token["access_token"]

        # }
        token = str(Token.objects.create(user=user))
        print("token", type(token))
        request_data = {
            "email":user.email,
            "verification_token":token

        }
        sender = SendVerificationEmail(request_data)
        result = sender.send()
        quiz_taker_id = QuizTaker.objects.get(user=user).id
        result["quiz_taker_id"] = quiz_taker_id
        result["UID"] = user.UID
        print("result", result)
        return  JsonResponse(result)
        # else:
        #     return Response(serializer.data,status=400)           

class UserList(APIView):

    def post(self, request, format=None):
        print('API',request,request.data)
#             # authuser_data = {
#             #     "username": request.data["name"],
#             #     "email": request.data["email"],
#             #     "password": request.data["password"] if "password" in request.data else str(uuid.uuid4())
#             # }
#             AuthUser.objects.create_user(** authuser_data)
#             # authuser.save()
#             print("CREATE")
#             # return Response( "CREATED")
#             if User.objects.filter(UID=request.data['UID']).exists():
#                 query_set = User.objects.get(UID=request.data['UID'])
#                 serializer = UserStrageSerializer(query_set)
#                 return Response(serializer.data,status=202)
#             else:
#                 print("else")
#                 try:
#                     user_status = copy.deepcopy(request.data["quiz_taker"][2])
#                     grade = copy.deepcopy(request.data["quiz_taker"][0])
#                     serializer = UserSerializer(data=request.data)
#                     if serializer.is_valid():
#                         serializer.save()
#                         print('saveed')
#                         quiz_taker = dict(serializer.data['quiz_taker'][0])
#                         quiz_taker_object = QuizTaker.objects.get(id=quiz_taker['id'])
#                         parent_quiz = ParentQuiz.objects.get(id=grade['grade'])
#                         for i in user_status["user_status"]:
#                             parent_status = ParentStatus.objects.get(id=i['status'])
#                             UserStatus.objects.create(
#                                 quiz_taker=quiz_taker_object,
#                                 status=parent_status,
#                                 grade=parent_quiz,
#                                 is_correct=i['isCorrect'],
#                                 is_false=i['isFalse'])
#                         return Response(serializer.data)
#                     else:
#                         raise Http404
#                 except Exception as e:
#                     print("EXCEPTION",)
#                     if e.args[0] == 'quiz_taker':
#                         serializer = UserSerializer(data=request.data)
#                         if serializer.is_valid():
#                             serializer.save()
#                             return Response(serializer.data)
#                         else:
#                             raise Http404
#                     else:
#                         raise e


class UserAllList(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer

class UserExist(APIView):
    permission_classes = ([AllowAny])
    def post(self, request, format=None):
        result = User.objects.filter(email=request.data["email"]).exists()
        return JsonResponse({"exists":True if result else False}, status=200)            


class OwnerOnlyRestriction(UserPassesTestMixin):
    '''
    restriction of owner user can access the user data
    '''
    def test_func(self):
        owner_user = self.request.user
        object_user = self.get_object()
        print("owner",owner_user, "object",object_user)
        verification = True if owner_user.is_staff or owner_user==object_user else False
        return verification
    
    def handle_no_permission(self):
        return JsonResponse({"info":"not allowed"},status=403)


class PasswordChange(APIView):
    def post(self, request, format=None):
        password = request.data.get("data")["password"]
        token = request.data.get("data")["token"]
        print("password-change", password, token)
        try:
            user = User.objects.get(auth_token=token)
            print(user)
            if not user:
                return JsonResponse({"password_change":False}, status=200)
            user.set_password(password)
            user.save()
            auth_token = Token.objects.get(user=user)
            auth_token.delete()
            token = get_tokens_for_user(user)
            return JsonResponse({"password_change":True, "tokens":token}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"password_change":False}, status=200)


class SendPasswordChange(APIView):
    permission_classes = ([AllowAny])

    def post(slef, request, format=None):
        print("PASSRE",request.data.get("data"))
        email = request.data.get("data")
        user = User.objects.get(email=email)
        if not user:
            return JsonResponse("no user")
        try:
            token = Token.objects.get(user=user)
            print("TOKEN_EXIST???",token)
            token.delete()
        except Exception as e:
            print("token doesn't exist", e)
        finally:
            token = str(Token.objects.create(user=user))
            print("token", token)
            request = {
                "email":user.email,
                "verification_token":token,
                "title":"[neko-japanese]password-change"

            }
            sender = SendPasswordReset(request)
            result = sender.send()
            print("result", result)
            return  JsonResponse(result)


class EmailVerify(APIView):
    # authentication_classes = ([J])
    # permission_classes = ([IsAuthenticated])
    def post(self, request, format=None):
       
        token = request.data.get("data")
        try:
            user = User.objects.get(auth_token=token)
            if not user:
                return JsonResponse({"verification":False}, status=200)
            user.is_active = True
            auth_token = Token.objects.get(user=user)
            auth_token.delete()
            user.save()
            token = get_tokens_for_user(user)
            return JsonResponse({"verification":True, "tokens":token}, status=200)
        except:
            return JsonResponse({"verification":False}, status=200)

class SetTestTakenAndOffset(APIView):
    def patch(self, request, format=None):
        try:
            request = request.data.get("data")
            import datetime
            from django.utils import timezone
            UID = request["UID"]
            test_taken = request["test_taken"]
            date_offset = int(request["date_offset"]) * -1
            user = User.objects.get(UID=UID)
            user.test_taken = test_taken
            user.date_offset = date_offset
            # date_local_now = timezone.now() + datetime.timedelta(minutes=date_offset)
            # user.test_taken_at = date_local_now
            user.test_taken_at = timezone.now()            
            user.save()
            return JsonResponse({"success":True}, status=200)
        except KeyError as e:
            return JsonResponse({"success":False, 'error-type':"Key Error","error":e.__str__() }, status=400)
        except Exception as e:
            return JsonResponse({"success":False, 'error':e.__str__()}, status=400)



class ResendEmailVerification(APIView):
    # not test yet
    def post(self, request, format=None):
        UID = request.data["UID"]
        user = User.objects.get(UID=UID)
        if not user:
            return JsonResponse("no user")
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Exception as e:
            print("no token",e)
        finally:
            token = str(Token.objects.create(user=user))
            request = {
                "email":user.email,
                "verification_token":token

            }
            sender = SendVerificationEmail(request)
            result = sender.send()
            return  JsonResponse(result)

class CheckTokenExist(APIView):
    def post(slef, request, format=None):
        print("PASSRE",request.data)
        token = request.data.get('token')
        try:
            token = Token.objects.get(key=token)
            return JsonResponse({"exist":True})
        except Exception as e:
            print("no token",e)
            return JsonResponse({"exist":False})


class UserDetailPatch(generics.RetrieveUpdateAPIView):
    '''this API is only for patching User.thumbnail
    '''
    pagination_class = None
    queryset =  User.objects.all()
    serializer_class = UserStrageSerializer
    lookup_field = 'UID'

    def perform_update(self, serializer):
        image = self.request.data['thumbnail']
        size=(80, 80)
        img = Image.open(image)
        format = img.format
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format, quality=85)
        instance = self.get_object()
        if instance.sns_thumbnail:
            instance.sns_thumbnail = ''
        thumbnail = File(thumb_io, name=image.name)
        serializer.save(thumbnail=thumbnail)


class UserDetail(OwnerOnlyRestriction,generics.RetrieveUpdateAPIView ): #this is for get user detail
    # parser_classes = (MultiPartParser, FormParser)
    pagination_class = None
    # authentication_classes = ([JWTAuthentication])
    permission_classes = ([AllowAny])
    # permission_classes = ([IsAuthenticated])
    queryset =  User.objects.all()
    # queryset = User.objects.prefetch_related(
    #     'question',
    #     'answer',
    #     'user_tag',
    #     'user_tag__tag',
    #     'favorite_question',
    #     'favorite_question__question',
    #     'liked_num',
    #     'liked_answer',
    #     'quiz_taker',
    #     'quiz_taker__grade',
    #     'quiz_taker__user_status',
    #     'quiz_taker__user_status__status',
    #     'my_quiz',
    #     'my_quiz__my_question',
    #     'my_quiz__my_question__question',
    #     'my_quiz__my_question__question__field',
    #     'my_quiz__my_question__question__status',
    #     )
    serializer_class = UserStrageSerializer
    lookup_field = 'UID'
    def get_object(self):

       
       
        queryset = self.get_queryset()
       
        filter = {}
        filter[self.lookup_field] = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, **filter)
        if obj.test_taken:
            # "check date for test_taken"
            import datetime
            from django.utils import timezone
            date_local_now = timezone.now() + datetime.timedelta(minutes=obj.date_offset)
            date_local_test_taken_at = obj.test_taken_at + datetime.timedelta(minutes=obj.date_offset)
            differDate = date_local_now - date_local_test_taken_at
            if differDate.days > 0:
                obj.test_taken = False
                obj.save()
                return obj 
            elif DateCalculations(date_local_now, date_local_test_taken_at) == False:
                obj.test_taken = False
                obj.save()
                return obj
            return obj 
        return obj


def DateCalculations(date_now, test_taken_at):
    # recieve date objects. this is for calculations for test_taken purpose.
    # at this point, date_now is supposed to be later than test_taken_at.
    if date_now.day != test_taken_at.day:
        return False if date_now.hour >= 5 else True
    else:
        # take a test between 0AM to 4:59am to be true or later to be false
        return False if test_taken_at.hour <= 4 else True