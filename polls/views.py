from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse


# Create your views here.
def index(request):
    # 1
    # return HttpResponse("Hello world.")
    
    # 2 데이터 직접 가져오기
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 3 templates 사용
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list, # context를 통해서 템플릿에 데이터를
    # }
    # return HttpResponse(template.render(context, request)) 
    
    # 4 render 함수로 간단히
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)



def detail(request, question_id):
    # 1 데이터 직접 가져오기
    # return HttpResponse("You're looking at question %s." % question_id)
    
    # 2 404에러 일으키기
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist.")
    # return render(request, 'polls/detail.html', {'question': question})
    
    # Shortcut으로 404에러 간단히 작성하기
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})



def results(request, question_id):
    # 1 데이터 직접 가져오기
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    
    # 2
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})



def vote(request, question_id):
    # 1 데이터 직접 가져오기
    # return HttpResponse("You're voting on question %s." % question_id)
    
    # 2 제출된 데이터를 처리하고 그 데이터로 무언가를 수행함
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # 외래키
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
