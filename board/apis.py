from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
from django.db.models import Count

from django.db.models import F
from django.db.models import Q
from django.db.models import Max
from django.db.models import Prefetch

import random
import operator
import copy
from itertools import chain



from django.http import Http404

from board.models import (
    BoardQuestion, 
    BoardAnswer, 
    BoardReply, 
    BoardQuestionLiked, 
    BoardAnswerLiked,
    BoardParentCenterTag, 
    BoardUserTag, 
    BoardCenterTag, 
    User,
    UserFavoriteQuestion,
    EachFavoriteQuestion
    )
from board.serializers import (
    BoardQuestionListSerializer, 
    BoardAnswerReadSerializer, 
    BoardAnswerCreateSerializer, 
    BoardReplyCreateSerializer, 
    BoardReplyReadSerializer, 
    BoardQuestionCreateSerializer, 
    BoardLikedCreateSerializer, 
    BoardLikedReadSerializer, 
    AnswerLikedReadSerializer, 
    ParentTagSerializer, 
    UserTagSerializer, 
    CenterTagSerializer, 
    FavoriteQuestionSerializer, 
    ReplyOnAnswerSerializer,
    AnswerAndReplyOnQuestionSerializer,
    BoardQuestionDetailSerializer,
    FavoriteQuestionDetailSerializer,
    UserTagNameSerializer,
    EachFavoriteQuestionSerializer,
    # CenterOnlyTagSerializer
    )


class BoardQuestionList(generics.ListAPIView):
    queryset = BoardQuestion.objects.prefetch_related(#cant solve two duplicate
        Prefetch('answer', queryset=BoardAnswer.objects.prefetch_related('reply__user')),
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        # 'answer__reply',
        # 'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )
        
    serializer_class = BoardQuestionListSerializer
    pagination_class = PageNumberPagination


class ViewedOrderedQuestion(generics.ListAPIView):
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        # 'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        ).order_by('-viewed')
        
    serializer_class = BoardQuestionListSerializer
    pagination_class = PageNumberPagination


class BoardQuestionCreate(APIView):
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__question__tag__parent_tag',
        'answer__reply',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )

    def post(self, request):
        liked_num_data = request.data.pop('liked_num')
        tag_data = request.data.pop('tag')
        user_id = request.data.pop('user')
        user = User.objects.get(UID=user_id)
        question = self.queryset.create(user=user, **request.data)
        for tag in tag_data:
            question.tag.add(tag)
            if BoardUserTag.objects.filter(tag=tag, user=user).exists():
                BoardUserTag.objects.update_or_create(
                    tag=tag,
                    user=user,
                    defaults={'used_num':F('used_num') + 1})
                print("if done")
            else:
                BoardUserTag.objects.create(tag=tag, user=user, used_num=1)
        BoardQuestionLiked.objects.create(question=question, **liked_num_data)
        return JsonResponse({"success":True}, status=200)


class BoardQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__question__tag__parent_tag',
        'answer__question__tag',
        'answer__reply',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )

    serializer_class = BoardQuestionDetailSerializer
    lookup_field = 'slug'


class BoardAnswerRead(generics.ListAPIView):
    queryset = BoardAnswer.objects.select_related(
        'user',
        'question',
        ).prefetch_related(
            'question__tag',
            'reply',
            'reply__answer',
            'reply__user',
            'liked_answer',
            'liked_answer__user',
            'liked_answer__answer',)

    serializer_class = BoardAnswerReadSerializer
    pagination_class = None


class BoardAnswerCreate(APIView):
    def post(self, request):
        try:
            question_id = request.data.pop('question')
            question = BoardQuestion.objects.get(id = question_id)
            user_uid = request.data.pop('user')
            user = User.objects.get(UID=user_uid)
            answer = answer = BoardAnswer.objects.create(question=question, user=user, **request.data)
            liked_answer = BoardAnswerLiked.objects.create(answer=answer)
            answer.liked_answer.set([liked_answer])
            serializer = BoardAnswerReadSerializer(answer)
            return Response(serializer.data)
        except:
            raise Http404



class BoardAnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardAnswer.objects.select_related(
        'user',
        'question',
        ).prefetch_related(
            'question__tag',
            'reply',
            'reply__answer',
            'reply__user',
            'liked_answer',
            'liked_answer__user',
            'liked_answer__answer')
    serializer_class = BoardAnswerCreateSerializer
    lookup_field = 'id'


class BoardReplyRead(generics.ListAPIView):
    queryset = BoardReply.objects.select_related(
        'user',
        'answer',
        )
    serializer_class = BoardReplyReadSerializer
    pagination_class = None


# class BoardReplyCreate(generics.CreateAPIView):
#     queryset = BoardReply.objects.select_related(
#         'user',
#         'answer',
#         )
#     serializer_class = BoardReplyReadSerializer

class BoardReplyCreate(APIView):
    def post(self, request):
        try:
            answer_id = request.data.pop('answer')
            user_uid = request.data.pop('user')
            user = User.objects.get(UID=user_uid)
            answer = BoardAnswer.objects.get(id=answer_id)
            reply = BoardReply.objects.create(answer=answer, user=user, **request.data)
            serializer = BoardReplyReadSerializer(reply)
            return Response(serializer.data)
        except:
            raise Http404


class QuestionLikedRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardQuestionLiked.objects.select_related(
        'question',
        ).prefetch_related(
            'user'
        )
    serializer_class = BoardLikedCreateSerializer


class AnswerLikedRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardAnswerLiked.objects.select_related(
        'answer',
        ).prefetch_related(
            'user'
        )
    serializer_class = AnswerLikedReadSerializer
    

class ParentTagList(generics.ListAPIView):
    queryset = BoardParentCenterTag.objects.prefetch_related(
            'center_tag',
            'center_tag__parent_tag',
        )
    serializer_class = ParentTagSerializer
    pagination_class = None


class CenterTagList(generics.ListAPIView):
    queryset = BoardCenterTag.objects.select_related(
        'parent_tag',
        ).prefetch_related(
            'question',
            )
    serializer_class = CenterTagSerializer
    pagination_class = None


# class CenterOnlyTagList(generics.ListAPIView):
#     queryset = BoardCenterTag.objects.all()
#     serializer_class = CenterOnlyTagSerializer
#     pagination_class = None


class UsertagCreate(generics.CreateAPIView):
    queryset = BoardUserTag.objects.all()
    serializer_class = UserTagSerializer


class UsertagRead(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardUserTag.objects.select_related('tag','user')
    serializer_class = UserTagSerializer


class UsertagForAUser(GenericAPIView):
    serializer_class = UserTagNameSerializer
    queryset = BoardUserTag.objects.select_related('tag')

    def get(self, request, format=None):
        user = request.query_params["user"]
        try:
            queryset  = self.queryset.filter(user=user)
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response(data)
        except BoardCenterTag.DoesNotExist as e:
            raise Http404



class FavoriteQuestionUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFavoriteQuestion.objects.select_related('user').prefetch_related(
        'question',
        'question__question',
        'question__question__tag',
        )
    serializer_class = FavoriteQuestionDetailSerializer
    lookup_field = 'user'


class FavoriteQuestionCreate(generics.CreateAPIView):
    queryset = UserFavoriteQuestion.objects.all()
    serializer_class = FavoriteQuestionSerializer



# class AnsweredQuestionList(generics.ListAPIView):
    # serializer_class = BoardQuestionListSerializer

    # def get_queryset(self):
    #     user = User.objects.filter(user=self.request.user)
    #     return BoardQuestion.objects.filter(UID=user)


class AnsweredQuestionList(GenericAPIView):
# get questions from user UID in answer
    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    queryset = BoardQuestion.objects.prefetch_related(
        Prefetch("answer",queryset=BoardAnswer.objects.select_related('user').all(),to_attr="answer_user"),
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        # 'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        ).order_by('-answer__on_best'
        ).order_by('-created_on')
    
    
    def get(self, request, format=None):
        user = request.query_params.getlist("user")
        def sorting(each):
            for i in each.answer.all():
                if i.user.UID == user[0]:
                    return i.on_best if i.on_best else i.on_reply
        try:
            question_queryset = [question for question in self.queryset.all() if [u for u in question.answer_user if u.user.UID == user[0]]]
            # get user answered questions
            sorted_queryset = sorted(question_queryset, key=sorting, reverse=True)
            # sort by question_answer.on_best or on_reply

            page = self.paginate_queryset(sorted_queryset)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class TagQuestionList(GenericAPIView):
# get questions from user UID in answer
    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        # 'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )

    def get(self, request, format=None):
        tag = request.query_params.getlist("tag")
        try:
            question_queryset  = self.queryset.filter(
                tag = tag[0],
            ).order_by('-solved').order_by('-created_on')
            page = self.paginate_queryset(question_queryset)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class favoriteQuestionList(GenericAPIView):
# get questions from user UID in answer
    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        # 'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )

    def get(self, request):
        print("request45",request)
        question_id = request.query_params.getlist("question_id")[0].split(",")
        print('ids',question_id)
        try:
            question_queryset = [question for question in self.queryset.all() if str(question.id) in question_id]
            page = self.paginate_queryset(question_queryset)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            print("data",data)
            return Response(data)
        except BoardQuestion.DoesNotExist:
            raise Http404



class EachFavoriteQuestionCreate(GenericAPIView):
    serializer_class = EachFavoriteQuestionSerializer
    queryset = EachFavoriteQuestion.objects.prefetch_related('question')

    def post(self, request):
        try:
            user = User.objects.get(UID=request.data.pop("UID"))
            question_id = request.data.pop("question")
            question = BoardQuestion.objects.get(id=question_id)
            if EachFavoriteQuestion.objects.filter(user=user, question=question).exists():
                EachFavoriteQuestion.objects.filter(user=user, question=question).delete()
                serializer = EachFavoriteQuestionSerializer()
                return Response(serializer.data)
            else:
                each_favorite_question = EachFavoriteQuestion.objects.create(user=user,question=question)
                serializer = EachFavoriteQuestionSerializer(each_favorite_question)
                return Response(serializer.data)
        except Exception as e:
            print("ERROR", e)
            raise Http404


class FavoriteQuestionList(GenericAPIView):
# get questions from user UID in answer
    pagination_class = PageNumberPagination
    serializer_class = EachFavoriteQuestionSerializer
    queryset = EachFavoriteQuestion.objects.prefetch_related(
        'question',
        'question__answer',
        'question__tag',
        'question__tag__parent_tag',
        'question__user',
        'question__liked_num',
        'question__liked_num__user',
        'question__liked_num__question',
        )
    
    def get(self, request, format=None):
        try:
            user_UID = request.GET.get('UID','')
            question_queryset = self.queryset.filter(user_id=user_UID)
            page = self.paginate_queryset(question_queryset)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        except Exception as e:
            print("ERROR",e)
            raise Http404

class UserQuestionList(GenericAPIView):
    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        ).order_by('-on_reply','-on_answer','-created_on')

    def get(self, request):
        uid = request.query_params.getlist("uid")[0]
        try:
            user_question_queryset = [question for question in self.queryset.all() if question.user.UID == uid]
            page = self.paginate_queryset(user_question_queryset)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        except BoardQuestion.DoesNotExist:
            raise Http404

class PatchBestAsnwer(APIView):
    def patch(self, request):
        question_id = request.data["question"]
        answer_id = request.data["answer"]
        question = BoardQuestion.objects.get(id=question_id)
        question.solved = True
        answer = BoardAnswer.objects.get(id=answer_id)
        answer.best = True
        answer.on_best = True
        question.save()
        answer.save()
        result = BoardQuestionListSerializer(question)
        return JsonResponse(result.data)


# class BestAsnweredQuestion(APIView, PageNumberPagination):
#     # pagination_class = PageNumberPagination

#     def post(self, request):
#         user_uid = request.data["uid"]
#         answers = BoardAnswer.objects.filter(user__UID=user_uid,best=True)
#         best_answered_question_ids = []
#         for i in answers:
#             best_answered_question_ids.append(i.question.id)
#         questions = BoardQuestion.objects.filter(id__in=best_answered_question_ids)
#         page = self.paginate_queryset(questions, request)
#         serializer = BoardQuestionListSerializer(page, many=True)
#         result = self.get_paginated_response(serializer.data)

#         return Response(result.data)


class RelatedQuestionList(GenericAPIView):
    """recieve 1 ~ 3 tag_ids and UID. get queryset exclude UID question 
    and filtered tag_id and solved status. then go to set_random_question function"""
    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    # queryset = BoardQuestion.objects.all()
    queryset = BoardQuestion.objects.prefetch_related(
        "tag__parent_tag",
        "answer__question",
        'answer__reply__user',
        'answer__reply__answer',
        'answer__user',
        'answer__liked_answer__user',
        'liked_num__user',
    ).select_related("user")

    def get(self, request, format=None):
        request_tag_list = request.query_params.getlist("tag")
        uid = request.query_params.get("uid")
        print('UID+CHECK', uid)
        q = self.queryset.all().exclude(user=uid).filter(
                tag__in = request_tag_list,
            )
        try:
            solved_queryset = [i for i in q if i.solved]
            unsolved_queryset = [i for i in q if i.solved==False]
            question = set_random_object(solved_queryset, unsolved_queryset)
            page = self.paginate_queryset(question)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        except BoardQuestion.DoesNotExist:
            raise Http404


class SearchQuestionList(GenericAPIView):
    """ this is for search question.
    if len(request.data) == 1, search title, descroption, also 
    answer descrption and reply description 
    if len(request.data) > 1 search questions with first 2 keywords
    that have both on title or description, if no, search questions which
    has one of them.
    after that, search in the question searched above with third key
    if con't find any, forth key will be searched in the second round question list
    if fond forth one will be searched in the third list with."""

    pagination_class = PageNumberPagination
    serializer_class = BoardQuestionListSerializer
    queryset = BoardQuestion.objects.prefetch_related(
        "tag", 
        "tag__parent_tag",
        'answer',
        'answer__question',
        'answer__question__user',
        'answer__question__tag',
        'answer__reply',
        'answer__reply__user',
        'answer__user',
        'answer__liked_answer',
        'answer__liked_answer__user',
        'liked_num',
        'liked_num__user',
        'liked_num__question',
        # 'liked_num__question__user',
        'liked_num__question__tag',
        ).select_related(
            'user'
        )
    


    def get(self, request, format=None):
        sorts_list = ['','solved', 'unsolved', 'liked', 'answered', 'viewed', 'new', 'old' ]
        sort = request.query_params.getlist("sort")[0]
        sort_index = sorts_list.index(sort)
        print()
        all_question = ''
        if sort_index:
            if sorts_list[sort_index] == 'solved':
                all_question = self.queryset.filter(solved=True)
                print("SOLVED",  all_question)
            elif sorts_list[sort_index] == 'unsolved':
                all_question = self.queryset.filter(solved=False)
            elif sorts_list[sort_index] == 'liked':
                all_question = self.queryset.all().order_by('-liked_num__liked_num')
            elif sorts_list[sort_index] == 'answered':
                all_question = self.queryset.all().annotate(
                    count_answer=Count('answer')
                ).order_by('-count_answer')
            elif sorts_list[sort_index] == 'viewed':
                all_question = self.queryset.all().order_by('-viewed')
            elif sorts_list[sort_index] == 'new':
                all_question = self.queryset.all().order_by('-created_on')
            elif sorts_list[sort_index] == 'old':
                all_question = self.queryset.all().order_by('created_on')
            else:
                all_question = self.queryset.all()
        else:
            all_question = self.queryset.all()
        keywords = request.query_params.getlist("keyword")[0]
        keywords = keywords.split(',')
        count = 0
        if len(keywords) < 2:
            question1 = all_question.filter(Q(title__icontains=keywords[0]) | Q(description__icontains=keywords[0])).distinct()
            question2 = all_question.filter(Q(answer__reply__description__icontains=keywords[0]) | Q(answer__description__icontains=keywords[0])).distinct()
            question = question1 | question2
            page = self.paginate_queryset(question)
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data)
        for keynum in range(len(keywords)):
            if count == 0:
                count += 1
            elif count == 1:
                question1 = all_question.filter(
                Q(title__icontains=keywords[0]) & Q(title__icontains=keywords[keynum]) 
                ).distinct()
                question2 = all_question.filter(
                Q(description__icontains=keywords[0]) & Q(description__icontains=keywords[keynum])
                ).distinct()
                question = question1 | question2
                if question.exists() == False:
                    question1 = all_question.filter(
                    Q(title__icontains=keywords[0]) | Q(title__icontains=keywords[keynum]) 
                    ).distinct()
                    question2 = all_question.filter(
                    Q(description__icontains=keywords[0]) | Q(description__icontains=keywords[keynum])
                    ).distinct()
                    question = question1 | question2
                submit_question = copy.deepcopy(question)
                count += 1
            elif count >= 2:
                temporary_question = copy.deepcopy(submit_question)
                submit_question = submit_question.filter(Q(title__icontains=keynum) | Q(description__icontains=keywords[keynum])).distinct()
                if submit_question.exists == False:
                    submit_question = temporary_question
                if count == len(keywords)-1 and submit_question.exists()==False:
                    submit_question = temporary_question
                    if temporary_question.exists() == False:
                        submit_question = question
        page = self.paginate_queryset(submit_question)
        serializer = self.get_serializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data)


# def get(self, request, format=None):
#         keywords = request.query_params.getlist("keyword")[0]
#         keywords = keywords.split(',')
#         all_question = self.queryset
#         count = 0
#         if len(keywords) < 2:
#             question1 = all_question.filter(Q(title__icontains=keywords[0]) | Q(description__icontains=keywords[0])).distinct()
#             question2 = all_question.filter(Q(answer__reply__description__icontains=keywords[0]) | Q(answer__description__icontains=keywords[0])).distinct()
#             question = question1 | question2
#             page = self.paginate_queryset(question)
#             if page is not None:
#                 serializer = self.get_serializer(page, many=True)
#                 result = self.get_paginated_response(serializer.data)
#                 data = result.data
#                 return Response(data)
#             else:
#                 serializer = self.get_serializer(question, many=True)
#                 return Response(serializer.data)
#         for keynum in range(len(keywords)):
#             print(keywords[keynum])
#             if count == 0:
#                 # question1 = all_question.filter(Q(title__icontains=key1) & Q(description__icontains=key2))
#                 count += 1
#             elif count == 1:
#                 question1 = all_question.filter(
#                 Q(title__icontains=keywords[0]) & Q(title__icontains=keywords[keynum]) 
#                 ).distinct()
#                 question2 = all_question.filter(
#                 Q(description__icontains=keywords[0]) & Q(description__icontains=keywords[keynum])
#                 ).distinct()
#                 question = question1 | question2
#                 if question.exists() == False:
#                     question1 = all_question.filter(
#                     Q(title__icontains=keywords[0]) | Q(title__icontains=keywords[keynum]) 
#                     ).distinct()
#                     question2 = all_question.filter(
#                     Q(description__icontains=keywords[0]) | Q(description__icontains=keywords[keynum])
#                     ).distinct()
#                     question = question1 | question2
#                 submit_question = copy.deepcopy(question)
#                 count += 1
#             elif count >= 2:
#                 temporary_question = copy.deepcopy(submit_question)
#                 submit_question = submit_question.filter(Q(title__icontains=keynum) | Q(description__icontains=keywords[keynum])).distinct()
#                 if submit_question.exists == False:
#                     submit_question = temporary_question
#                 if count == len(keywords)-1 and submit_question.exists()==False:
#                     submit_question = temporary_question
#                     if temporary_question.exists() == False:
#                         submit_question = question
#         page = self.paginate_queryset(submit_question)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             result = self.get_paginated_response(serializer.data)
#             data = result.data
#             return Response(data)
#         else:
#             serializer = self.get_serializer(submit_question, many=True)
#             return Response(serializer.data)

class UserAnswerAndQuestionApi(APIView):
    def get(self, request):
        print("request",request)
        user_UID = request.query_params['user']
        print("USER_UID",user_UID)
        try:
            question = BoardQuestion.objects.filter(user_id=user_UID).filter(Q(on_answer=True) | Q(on_reply=True)).all()
            answer  = BoardAnswer.objects.filter(
                 Q(user_id = user_UID) & (Q(on_reply=True) | Q(on_best=True))
                )
            serializer = AnswerAndReplyOnQuestionSerializer(question, many=True)
            serializer2 = ReplyOnAnswerSerializer(answer, many=True)
            union = list(chain([serializer.data], [serializer2.data]))
            print("ANSWER_AND_REPLY", serializer.data)
            print("REPLY_ON_ON", serializer2.data)
            print("UNION", union)
            return Response(union)
        except Exception as e :
            print("ERROR", e)
            raise Http404

# class Conbine():
#     def __init__(self, keywords=''):
#         string = ''
#         keywords = keywords

#     def __add__(self, other):
#         return self.string + other.string

# def conbine_Q(keywords):
#     filter_operator = {
#         "&": operator.and_,
#         "|": operator.or_
#     }
#     Q_filter = Q(title__icontains="{}").format() 
#     Q_dict = dict()
#     # for k in range(len(keywords)):
#     for i in keywords:
#         Q_dict[i] = Q(title__icontains="{i}").format() + filter_operator["&"]()


        # request_tag_list = request.query_params.getlist("tag")
        # try:
        #     solved_queryset = BoardQuestion.objects.filter(
        #         tag__in = request_tag_list,
        #         solved = True
        #     ).distinct()
        #     print("solved_queryset", solved_queryset)
        #     unsolved_queryset = BoardQuestion.objects.filter(
        #         tag__in = request_tag_list,
        #         solved = False
        #     ).distinct()
        #     question = set_random_object(solved_queryset, unsolved_queryset)
        #     # question = solved_queryset
        #     print(question)
        #     serializer = BoardQuestionListSerializer(question, many=True)
        #     return Response(serializer.data)
        # except BoardQuestion.DoesNotExist:
        #     raise Http404

# @api_view(['GET'])
# def search(request):
#     query = request.data.get('query', '')

#     if query:
#         question = BoardQuestion.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#         serializer = BoardQuestionListSerializer(question, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"products": []})


# set 3 unsolved questions and 12 solved questions
def set_random_object(solved_queryset, unsolved_queryset):
    print("in set_random")
    unsolevd_list = [i for i in unsolved_queryset]
    solved_list = [i for i in solved_queryset]
    
    if len(solved_queryset) >= 12:
        solved_queryset_num = 12
    else:
        solved_queryset_num = len(solved_queryset)

    if len(unsolved_queryset) >= 3:
        unsolved_queryset_num = 3
    else:
        unsolved_queryset_num = len(unsolved_queryset)
    # set 3 unsolved questions
    random_id_list = random.sample(unsolevd_list, unsolved_queryset_num)
    # set 12 solved questions
    random_solved_list = random.sample(solved_list, solved_queryset_num)
    for solved_question in random_solved_list:
        random_id_list.append(solved_question)
    return random_id_list


