from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from common.mixins import UserIsOwnerMixin
from goals.forms import HabitGoalUpdateForm
from goals.mixins import GoalFormValidMixin
from goals.models import HabitGoal, Category


class HabitGoalUpdateView(LoginRequiredMixin, UserIsOwnerMixin,GoalFormValidMixin , UpdateView):
    model = HabitGoal
    form_class = HabitGoalUpdateForm
    template_name = 'goals/create-form.html'



    def dispatch(self, request, *args, **kwargs):
        goal = self.get_object()
        if goal.is_completed:
            messages.warning(request, "You cannot edit completed goal")
            return redirect('habit-goal-details', pk=goal.pk)
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('habit-goal-details', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



