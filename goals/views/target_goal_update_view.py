from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from common.mixins import UserIsOwnerMixin
from goals.forms import TargetGoalUpdateForm
from goals.mixins import GoalFormValidMixin
from goals.models import TargetGoal, Category


class TargetGoalUpdateView(LoginRequiredMixin,UserIsOwnerMixin,GoalFormValidMixin,UpdateView):
    model = TargetGoal
    form_class = TargetGoalUpdateForm
    template_name = 'goals/create-form.html'


    def dispatch(self, request, *args, **kwargs):
        goal = self.get_object()
        if goal.is_completed:
            messages.warning(request, "You cannot edit completed goal")
            return redirect('target-goal-details', pk=goal.pk)
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('target-goal-details', kwargs={'pk': self.object.pk})