from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


from goals.models import TargetGoal


class TargetGoalDetailView(LoginRequiredMixin, DetailView):
    model = TargetGoal
    template_name = 'goals/goal-details.html'
    context_object_name = 'goal'

    def get(self, request, *args, **kwargs):
        storage = messages.get_messages(request)
        list(storage)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object

        total = goal.steps.count()
        current = goal.steps.filter(completed=True).count()

        context['progress_total'] = total
        context['progress_current'] = current
        context['progress'] = goal.progress_percent() if hasattr(goal, 'progress_percent') else 0


        return context
