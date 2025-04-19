from django.contrib import admin
from .models import Question, Answer, Tag, UserProfile, Comment, Vote

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'views', 'is_solved')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'is_accepted')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('content',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation', 'location')
    search_fields = ('user__username', 'location')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'get_parent')
    search_fields = ('content', 'author__username')

    def get_parent(self, obj):
        return obj.question or obj.answer
    get_parent.short_description = 'On'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'created_at', 'get_target')
    list_filter = ('value', 'created_at')

    def get_target(self, obj):
        return obj.question or obj.answer
    get_target.short_description = 'Voted on'
