from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpRequest,HttpResponse,Http404,HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from core.models import Question, Choise
from core.forms import QuestionCreateForm
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 
                  'index.html',
                  context={
                    'questions': Question.objects.order_by('-create_time').all()
                  }
                )

class HomeView(ListView):
    # queryset = Question.objects.all()
    # ordering = ['-create_time']
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        query: str = self.request.GET.get('q', '')
        if query.startswith('user:'):
            username = query.split(':')[1]
            return Question.objects.filter(user__username=username)
        if query.startswith('[') and query.endswith(']'):
            print()
        queryset = Question.objects.filter(question_text__icontains=query)
        return queryset.order_by('-create_time')
        
def about_viwe(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def contact_viwe(request: HttpRequest) -> HttpResponse:
    return render(request, 'contact.html')

class QuestionDetailView(DeleteView):
    model = Question
    queryset = Question.objects.all()
    template_name = 'core/question_detail.html'

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('core:home')
    template_name = 'core/question_delete.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()
        return Question.objects.filter(
            user=self.request.user
        )
    
class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'core/question_edit.html'
    fields = ['question_text']

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()
        return Question.objects.filter(
            user=self.request.user
        )
    

class ChoiseSelectView(LoginRequiredMixin,UpdateView):
    http_method_names = ['post']
    model = Choise
    fields = []
    def get_success_url(self) -> str:
        return self.object.question.get_absolute_url()
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object: Choise = self.get_object()
        self.object.votes += 1
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    




def question_choise_view(request: HttpResponse, pk: int) -> HttpResponse:
    if request.method == 'POST':
        choise_id: str | None = request.POST.get('choise')
        if choise_id is None:
            return HttpResponseBadRequest('<h1>Please select choice</h1>')
        if not choise_id.isdigit():
            return HttpResponseBadRequest('<h1>You naughty</h1>')
        
        choise_id = int(choise_id)
        try:
            choise: Choise = Choise.objects.get(pk=choise_id)
        except Choise.DoesNotExist:
            return HttpResponseBadRequest('<h1>You naughty</h1>')
        choise.votes += 1
        choise.save()
        return redirect('core:question-results',pk=choise.question.id)
    
    return render(
        request,
        'core/question_vote.html',
        context={
            'question': Question.objects.get(pk=pk)
        }
    )

def question_results_view(request: HttpResponse, pk: int) -> HttpResponse:
    return render(
        request,
        'core/question_results.html',
        context={
            'question': Question.objects.get(pk=pk)
        }
    )

class QuestionCreateView(LoginRequiredMixin,CreateView):
    form_class = QuestionCreateForm
    template_name = 'core/question_create.html'
    
    def get_success_url(self) -> str:
        return reverse('core:question-choises', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs
    
   
@login_required
def add_choises_to_question(request: HttpRequest, pk: int) -> HttpResponse:
    if not Question.objects.filter(user=request.user, pk=pk).exists() and not request.user.is_staff:
        raise Http404()
    question = get_object_or_404(Question,pk=pk)
    ChoiseInLineFormSet = inlineformset_factory(Question, Choise, fields=['choice_text'])
    if request.method == "POST":
        formset = ChoiseInLineFormSet(request.POST, request.FILES, instance=question)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        formset = ChoiseInLineFormSet(instance=question)
    return render(request,"core/question_choices.html", {"formset": formset})


