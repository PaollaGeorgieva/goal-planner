from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from common.mixins import UserIsOwnerMixin
from goals.models import TargetGoal


class TargetGoalDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = TargetGoal
    template_name = 'goals/delete-goal.html'
    success_url = reverse_lazy('goals')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.object
        return context