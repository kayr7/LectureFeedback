from django.contrib import admin

# Register your models here.


from .models import Question, Choice, Entity, TextResponse


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ('question', 'votes')
    search_fields = ('choice_text',)



@admin.register(TextResponse)
class TextResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'response_text_preview')
    list_filter = ('question',)
    search_fields = ('response_text',)

    def response_text_preview(self, obj):
        return obj.response_text[:50]  # Adjust slice as needed
    response_text_preview.short_description = "Response Preview"


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ('choice_text', 'votes')
    extra = 5
    can_delete = True



class QuestionInline(admin.TabularInline):
    model = Question
    fields = ['question_text', 'display_choices']
    readonly_fields = ['question_text', 'display_choices']
    extra = 0
    can_delete = False

    def display_choices(self, obj):
        choices = obj.choice_set.all()
        return ", ".join([f"{choice.choice_text} ({choice.votes} votes)" for choice in choices])
    display_choices.short_description = "Choices"



class EntityAdmin(admin.ModelAdmin):
    change_form_template = 'feedback_app/change_form.html'
    list_display = ('id', 'name')
    inlines = [QuestionInline]
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Custom logic to pass extra context to the admin template, like TextResponse data
        extra_context = extra_context or {}
        entity_questions = Question.objects.filter(entity__id=object_id).prefetch_related('choices')
        extra_context['entity_questions'] = entity_questions
        entity_questions = Question.objects.filter(entity__id=object_id)
        free_text_responses = TextResponse.objects.filter(question__in=entity_questions)
        extra_context['free_text_responses'] = free_text_responses
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'entity', 'question_type')  # To display entity in the question list
    list_filter = ['entity', 'question_type']  # To enable filtering by entity
    search_fields = ['question_text']  # Assuming you'd like a search feature

    fieldsets = [
        (None,               {'fields': ['entity', 'question_text', 'question_type']}),
    ]
    inlines = [ChoiceInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        if obj:  # obj will be None on the add page, and an instance on the change page
            if obj.question_type == 'FT':  # Adjust 'FT' as necessary
                self.inlines = []
            else:
                self.inlines = [ChoiceInline]
        return form


admin.site.register(Question, QuestionAdmin)
admin.site.register(Entity, EntityAdmin)