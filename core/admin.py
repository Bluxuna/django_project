from django.contrib import admin
from core.models import Question, Choise,Tag

# Register your models here.
admin.site.register([Tag])

class ChoiseInLine(admin.StackedInline):
    model = Choise
    extra = 1
    fields = ['choice_text', 'votes']
    readonly_fields = ['votes']

@admin.register(Question)
class QuestionAdminModel(admin.ModelAdmin):
    inlines = [ChoiseInLine]
    filter_horizontal = ['tags']
    list_display = ['question_text', 'create_time']
    search_fields = ['question_text', 'choice__text']