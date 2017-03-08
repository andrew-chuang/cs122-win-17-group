# 
#
#
#
#
#

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect

from .models import Question, Choice, Yelp_Input
from .forms import YelpForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

def index(request):
    questions=None
    if request.GET.get('search'):
        search = request.GET.get('search')
        questions = search

        name = request.GET.get('name')
        query = Yelp_Input.object.create(query=search, user_id=name)
        query.save()

    return render(request, 'polls/index.html',{
        'questions': questions,
    })


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
     # same as above, no changes needed.
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class YelpView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_yelp_inputs'

class VerifyView(generic.DetailView):
    model = Yelp_Input
    template_name = 'polls/verify.html'

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        try:
            user = Person.objects.get(name = search_id)
            #do something with user
            html = ("<H1>%s</H1>", user)
            return HttpResponse(html)
        except Person.DoesNotExist:
            return HttpResponse("no such user")  
    else:
        return render(request, 'polls/verify.html')

def get_rest1(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YelpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('verify.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YelpForm()

    return render(request, 'index.html', {'form': form})











