from django.contrib import admin
# import nested_admin
from .models import (
	Quiz, 
	Question, 
	Answer, 
	QuizTaker, 
	ParentQuiz,
	ParentField,
	ParentStatus,
	QuestionType,
	UserStatus,
	MyQuiz,
	MyQuestion
	)


# class AnswerInline(nested_admin.NestedTabularInline):
# 	model = Answer
# 	extra = 0
# 	amx_num =4


# class QuestionInline(nested_admin.NestedTabularInline):
# 	model = Question
# 	inlines = [AnswerInline,]
# 	extra = 5


# class QuizAdmin(nested_admin.NestedModelAdmin):
# 	inlines = [QuestionInline]


# class AnswerAdmin(nested_admin.NestedModelAdmin):
# 	inlines = [AnswerInline]


# class UserAnswerInline(admin.TabularInline):
# 	model = UsersAnswer


# class QuizTakerAdmin(admin.ModelAdmin):
# 	inlines = [UserAnswerInline,]


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker)
# admin.site.register(UsersAnswer)
admin.site.register(ParentQuiz)
admin.site.register(ParentField)
admin.site.register(ParentStatus)
admin.site.register(QuestionType)
admin.site.register(UserStatus)
admin.site.register(MyQuiz)
admin.site.register(MyQuestion)

