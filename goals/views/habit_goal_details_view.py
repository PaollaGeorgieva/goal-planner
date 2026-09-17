from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.views.generic import DetailView


from goals.models import HabitGoal, HabitCheck


class HabitGoalDetailView(LoginRequiredMixin, DetailView):
    model = HabitGoal
    template_name = 'goals/habit-details.html'
    context_object_name = 'goal'


    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object

        current = goal.get_current_period_checks()
        total = goal.target_per_period

        context['progress_total'] = total
        context['progress_current'] = current

        return context

    def post(self, request, *args, **kwargs):
        goal = self.get_object()
        today = timezone.localdate()
        current_checks = goal.get_current_period_checks(today=today)

        if goal.is_completed:
            messages.warning(
                request,
                "This habit is completed and cannot receive new check-ins."
            )
            return redirect('habit-goal-details', pk=goal.pk)

        if current_checks >= goal.target_per_period:
            messages.warning(
                request,
                f"You've already completed your target ({goal.target_per_period}) for this {goal.period_unit}.")
        else:
            HabitCheck.objects.create(habit=goal, date=today)
            remaining = goal.target_per_period - (current_checks + 1)
            message = f"Check-in successful! {remaining} remaining for this {goal.period_unit}." if remaining > 0 else "You've completed your goal for this period!"
            messages.success(request, message)

        return redirect('goals')

