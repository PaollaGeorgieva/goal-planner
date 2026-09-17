from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.contrib import messages

from goals.models import TargetGoal


class TargetGoalCompleteView(LoginRequiredMixin,  SingleObjectMixin, RedirectView):
    model = TargetGoal
    permanent = False
    http_method_names = ['post', 'options']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_completed=False)

    def post(self, request, *args, **kwargs):
        goal = self.get_object()
        try:
            goal.mark_as_completed()
            messages.success(self.request, f"Target goal “{goal.title}” marked as completed.")
        except ValueError as error:
            messages.error(self.request, str(error))
        return redirect('target-goal-details', pk=goal.pk)
