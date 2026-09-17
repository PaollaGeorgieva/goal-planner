
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import  redirect
from django.contrib import messages

from goals.models import HabitGoal

class HabitGoalCompleteView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    model = HabitGoal
    permanent = False
    http_method_names = ['post', 'options']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_completed=False)

    def post(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.mark_as_completed()
        messages.success(self.request, f"Habit goal “{goal.title}” marked as completed.")
        return redirect('habit-goal-details', pk=goal.pk)