from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from goals.forms import HabitGoalCreateForm, TargetGoalCreateForm
from goals.mixins import GoalFormValidMixin
from goals.models import Category


class GoalCreateView(LoginRequiredMixin, GoalFormValidMixin, CreateView):
    template_name = 'goals/create-form.html'
    success_url = reverse_lazy('goals')



    def get_form_class(self):
        goal_type = self.request.POST.get('goal_type') or self.request.GET.get('goal_type', 'target')
        if goal_type == 'habit':
            return HabitGoalCreateForm
        return TargetGoalCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal_type'] = self.request.POST.get('goal_type', 'target')

        return context

