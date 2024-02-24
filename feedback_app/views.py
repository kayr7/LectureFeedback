from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from .forms import SurveyForm
from .models import Question, Choice, Entity, TextResponse
from django.http import HttpResponse
from django.urls import reverse
import base64
from .tools import generate_qr_code


def feedback_view(request, entity_id):
    cookie_name = f'has_voted_{entity_id}'
    if cookie_name in request.COOKIES:
        return HttpResponse("Sie haben hier bereits feedback gegeben.")
    
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        return HttpResponse("Entity not found.")

    questions = Question.objects.filter(entity=entity)
    if request.method == 'POST':
        form = SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            for question in questions:
                if question.question_type == 'MC':
                    selected_choice = form.cleaned_data.get(f'question_{question.id}')
                    selected_choice.votes += 1
                    selected_choice.save()
                elif question.question_type == 'FT':
                    response_text = form.cleaned_data.get(f'question_{question.id}')
                    TextResponse.objects.create(question=question, response_text=response_text)
            
            response = redirect('feedback_success')  # You need to define this view and URL
            response.set_cookie(f'has_voted_{entity_id}', 'yes', max_age=3600*24*365*2)  # Set cookie for 2 years
            return response

    else:
        form = SurveyForm(questions=questions)
    return render(request, 'feedback_app/survey.html', {'form': form})



def entities_overview(request):
    entities = Entity.objects.all()
    return render(request, 'feedback_app/entities_overview.html', {'entities': entities})




def feedback_success(request):
    return HttpResponse("Vielen Dank fuer das Feedback!")

def entity_qr_code(request, entity_id):
    entity = get_object_or_404(Entity, pk=entity_id)
    feedback_url = request.build_absolute_uri(reverse('feedback', args=[entity_id]))  # Adjust 'entity_feedback' to your URL name
    qr_code_image = generate_qr_code(feedback_url)

    # Convert QR code image to data URI so it can be displayed directly in the template
    data_uri = f"data:image/png;base64,{base64.b64encode(qr_code_image.getvalue()).decode('utf-8')}"
    return render(request, 'feedback_app/entity_qr_code.html', {'entity': entity, 'qr_code_data_uri': data_uri})




