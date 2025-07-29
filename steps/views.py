import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from common.mixins import UserIsOwnerMixin
from goals.models import TargetGoal
from steps.forms import StepCreateForm
from steps.mixins import GoalContextMixin
from steps.models import Step


from django.views import View
class StepsView(LoginRequiredMixin, GoalContextMixin, ListView):
    model = Step
    template_name = 'steps/steps.html'
    context_object_name = 'steps'

    def get(self, request, *args, **kwargs):

        storage = messages.get_messages(request)
        list(storage)
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        return self.goal.steps.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.goal
        context['total_steps'] = self.goal.steps.count()
        context['completed_steps'] = self.goal.steps.filter(completed=True).count()
        context['progress'] = self.goal.progress_percent()
        return context


class StepCreateView(LoginRequiredMixin, GoalContextMixin, CreateView):
    model = Step
    form_class = StepCreateForm
    template_name = 'steps/add-step.html'
    goal_model = TargetGoal

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self.goal.is_completed:
            messages.error(request, "You cannot add a step to a completed goal.")
            return redirect('steps:step-list', pk=self.goal.pk)
        return response


    def form_valid(self, form):
        form.instance.target_goal = self.goal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('steps:step-list', kwargs={'pk': self.goal.pk})


class StepToggleCompleteView(LoginRequiredMixin, GoalContextMixin, View):


    def post(self, request, *args, **kwargs):
        if self.goal.is_completed:
            messages.error(request, "You cannot edit a step in a completed goal.")
            return redirect('steps:step-list', pk=self.goal.pk)

        step_id = kwargs.get('step_id')
        step = get_object_or_404(Step, pk=step_id, target_goal=self.goal)
        step.completed = not step.completed
        step.save()
        return redirect('steps:step-list', pk=self.goal.pk)


class StepEditView(LoginRequiredMixin, GoalContextMixin, UpdateView):
    model = Step
    form_class = StepCreateForm
    template_name = 'steps/add-step.html'
    pk_url_kwarg = 'step_id'
    goal_model = TargetGoal

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if self.goal.is_completed:
            messages.error(request, "You cannot edit a step in a completed goal.")
            return redirect('steps:step-list', pk=self.goal.pk)

        return response

    def get_success_url(self):
        return reverse('steps:step-list', args=[self.goal.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.goal
        return context


class StepDeleteView(LoginRequiredMixin, DeleteView):
    model = Step

    def get_object(self, queryset=None):
        goal = get_object_or_404(TargetGoal, pk=self.kwargs['pk'], user=self.request.user)
        step = get_object_or_404(Step, pk=self.kwargs['step_id'], target_goal=goal)
        return step

    def get(self, request, *args, **kwargs):
        return redirect('steps:step-list', pk=kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return redirect('steps:step-list', pk=kwargs['pk'])