from rest_framework import serializers,exceptions
from user.models import User, IPData
from board.serializers import (
    BoardAnswerReadSerializer, 
    BoardAnswerStorageSerializer,
    BoardQuestionListSerializer, 
    BoardQuestionStorageSerializer,
    BoardLikedReadSerializer, 
    BoardLikedStorageSerializer,
    AnswerLikedCreateSerializer, 
    AnswerLikedStorageSerializer,
    UserTagReadSerializer, 
    UserTagStorageSerializer,
    FavoriteQuestionReadSerializer,
    FavoriteQuestionStorageSerializer,
    )
from board.models import BoardQuestion, BoardAnswer
from quiz.models import User, QuizTaker, UserStatus, ParentQuiz, ParentStatus, MyQuiz
from quiz.serializers import QuizTakerSerializer,QuizTakerStorageSerializer, MyQuizSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.registration.serializers  import complete_social_login
from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.conf import settings
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _

# from allauth.account.views import EmailView

class IPDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPData
        fields = '__all__'

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)
        print("CCLIOGIN",username, email, password)
        if not user:
            if User.objects.filter(email=email).exists():
                msg = _('wrong-password.')
            else:
                msg = _('user-not-found.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs

    def get_auth_user(self, username, email, password):
        
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.
        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:

            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = _('from get_auth provided credentials.')
                raise exceptions.ValidationError(msg)
        print("CLOGIN")
        return self.get_auth_user_using_orm(username, email, password)
    # def get_cleaned_data(self):
    #     print("CR",self.validated_data )
    #     super(CustomLoginSerializer, self).get_cleaned_data()
    #     return {
    #         'email': self.validated_data.get('email', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #     }


class CustomRegisterSerializer(RegisterSerializer):

    def get_cleaned_data(self):
        print("CR",self.validated_data )
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }
        




# from rest_framework_simplejwt.tokens import RefreshToken

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
# class GoogleRegisterSerializer(SocialLoginSerializer):
#     print("KOKOKO",SocialLoginSerializer)

#     def save(self, request):
#         print('self',self,'requwst', request)

#     def validate(self, attrs):
#         view = self.context.get('view')
#         request = self._get_request()
#         print('view',view,'request',request)
#         print('self',self,'attrs',attrs)
#         adapter_class = getattr(view, 'adapter_class', None)
#         if not adapter_class:
#             raise serializers.ValidationError(_("Define adapter_class in view"))

#         adapter = adapter_class(request)
#         app = adapter.get_provider().get_app(request)
#         if attrs.get('access_token'):
#             access_token = attrs.get('access_token')
        
#         social_token = adapter.parse_token({'access_token': access_token})
#         social_token.app = app

#         login = self.get_social_login(adapter, app, social_token, access_token)
#         complete_social_login(request, login)

#         attrs['user'] = login.account.user
#         print("USER", attrs['user'].__dir__())
#         return attrs

    class Meta:
        model = User
        fields = "__all__"

class QuestionForUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = BoardQuestion
        fields = [
            'id',
        ]

class AnswerForUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = BoardAnswer
        fields = [
            'id',
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    question = BoardQuestionListSerializer(many=True, required=False) #ForeignKey
    answer = BoardAnswerReadSerializer(many=True, required=False) #ForeignKey
    liked_num = BoardLikedReadSerializer(many=True, required=False) #ManyToManyField
    liked_answer = AnswerLikedCreateSerializer(many=True, required=False) #ManyToManyField
    user_tag = UserTagReadSerializer(many=True, required=False) #ForeignKey
    favorite_question = FavoriteQuestionReadSerializer(many=True, required=False) #ForeignKey
    quiz_taker = QuizTakerSerializer(many=True, required=False) #ForeignKey
    ip_data = IPDataSerializer(many=True,required=False) #ForeignKey
    my_quiz = MyQuizSerializer(many=True,required=False) #ForeignKey

    class Meta:
        model = User
        fields = ["UID",
                  "username", 
                  "thumbnail",
                  "question", 
                  "answer",
                  "liked_num",
                  "liked_answer",
                  "user_tag",
                  "favorite_question",
                  "quiz_taker",
                  "my_quiz",
                  "created_on"
                  ]

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data["username"],
#             validated_data['email'],
#             validated_data['password']
#         )
#         return user

    
class UserSerializer(serializers.ModelSerializer):
    question = BoardQuestionListSerializer(many=True, required=False) #ForeignKey
    answer = BoardAnswerReadSerializer(many=True, required=False) #ForeignKey
    liked_num = BoardLikedReadSerializer(many=True, required=False) #ManyToManyField
    liked_answer = AnswerLikedCreateSerializer(many=True, required=False) #ManyToManyField
    user_tag = UserTagReadSerializer(many=True, required=False) #ForeignKey
    favorite_question = FavoriteQuestionReadSerializer(many=True, required=False) #ForeignKey
    quiz_taker = QuizTakerSerializer(many=True, required=False) #ForeignKey
    # ip_data = IPDataSerializer(many=True,required=False) #ForeignKey
    my_quiz = MyQuizSerializer(many=True,required=False) #ForeignKey
    # all_auth = EmailView(many=True,required=False)
    
    
    
    class Meta:
        model = User
        fields = [
            "UID",
            "username", 
            "thumbnail",
            "question", 
            "answer",
            "liked_num",
            "liked_answer",
            "user_tag",
            "favorite_question",
            "quiz_taker",
            "my_quiz",
            "created_on"
        ]
        # read_only_field = []

    def create(self, validated_data):
        print("SERI", validated_data)
        try:
            quiz_taker = validated_data.pop('quiz_taker')
            print('quiz_taker',quiz_taker,'0',quiz_taker[0])
            level = dict(quiz_taker[1])['level']
            print('level',level)
            ip_data = validated_data.pop('ip_data')
            user = User.objects.create(**validated_data)
            MyQuiz.objects.create(user=user)
            QuizTaker.objects.create(user=user, level=level, **quiz_taker[0])
            IPData.objects.create(user=user, **ip_data[0])
            return user
        except:
            # set 超初級 ids 変わる可能性あり
            # 7 = ボキャブラリー
            # 1 = ひらがな
            # 6 = カタカナ
            # 13 = 数字
            # grade 4 = 超初級
            ids = ["ボキャブラリー","ひらがな","カタカナ","すうじ"]
            ip_data = validated_data.pop('ip_data')
            user = User.objects.create(**validated_data)
            print("USER_CREATED")
            MyQuiz.objects.create(user=user)
            IPData.objects.create(user=user, **ip_data[0])
            grade = ParentQuiz.objects.get(name="超初級")
            quiz_taker = QuizTaker.objects.create(user=user, grade=grade)
            status = ParentStatus.objects.filter(name__in=ids)
            for i in status:
                UserStatus.objects.create(quiz_taker=quiz_taker, status=i, grade=grade)
            return user


class UserStrageSerializer(serializers.ModelSerializer):
    # question = QuestionForUserSerializer(many=True, required=False) #ForeignKey
    # answer = AnswerForUserSerializer(many=True, required=False) #ForeignKey
    # liked_num = BoardLikedStorageSerializer(many=True, required=False) #ManyToManyField
    # liked_answer = AnswerLikedStorageSerializer(many=True, required=False) #ManyToManyField
    # user_tag = UserTagStorageSerializer(many=True, required=False) #ForeignKey
    # favorite_question = FavoriteQuestionStorageSerializer(many=True, required=False) #ForeignKey
    # quiz_taker = QuizTakerStorageSerializer(many=True, required=False) #ForeignKey
    # my_quiz = MyQuizSerializer(many=True,required=False) #ForeignKey
    
    class Meta:
        model = User
        fields = ["UID",
                  "username", 
                  "thumbnail",
                  "sns_thumbnail",
                #   "question", 
                #   "answer",
                #   "liked_num",
                #   "liked_answer",
                #   "user_tag",
                #   "favorite_question",
                #   "quiz_taker",
                #   "my_quiz",
                  "is_staff",
                  "is_active",
                  "test_taken",
                  "test_taken_at",
                  "created_on"
                  ]



class SimpleUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["UID",
                  "username", 
                  
                  ]
# class UserStrageSerializer(serializers.ModelSerializer):
#     question = BoardQuestionListSerializer(many=True, required=False) #ForeignKey
#     answer = BoardAnswerReadSerializer(many=True, required=False) #ForeignKey
#     liked_num = BoardLikedReadSerializer(many=True, required=False) #ManyToManyField
#     liked_answer = AnswerLikedCreateSerializer(many=True, required=False) #ManyToManyField
#     user_tag = UserTagReadSerializer(many=True, required=False) #ForeignKey
#     favorite_question = FavoriteQuestionReadSerializer(many=True, required=False) #ForeignKey
#     quiz_taker = QuizTakerSerializer(many=True, required=False) #ForeignKey
    
#     class Meta:
#         model = User
#         fields = ["UID",
#                   "name", 
#                   "thumbnail",
#                   "country",
#                   "question", 
#                   "answer",
#                   "liked_num",
#                   "liked_answer",
#                   "user_tag",
#                   "favorite_question",
#                   "quiz_taker"
#                   ]