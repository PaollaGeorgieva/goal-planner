from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView


from goals.models import HabitGoal, HabitCheck


class HabitGoalDetailView(LoginRequiredMixin, DetailView):
    model = HabitGoal
    template_name = 'goals/habit-details.html'
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

        current = goal.get_current_period_checks()
        total = goal.target_per_period

        context['progress_total'] = total
        context['progress_current'] = current

        return context

    def post(self, request, *args, **kwargs):
        goal = self.get_object()
        today = date.today()
        current_checks = goal.get_current_period_checks(today=today)

        if current_checks >= goal.target_per_period:
            (messages.warning(self.request,
                              f"You've already completed your target ({goal.target_per_period}) for this {goal.period_unit}."))
        else:
            HabitCheck.objects.create(habit=goal, date=today)
            remaining = goal.target_per_period - (current_checks + 1)
            msg = f"Check-in successful! {remaining} remaining for this {goal.period_unit}." if remaining > 0 else "You've completed your goal for this period!"
            messages.success(self.request, msg)

        return redirect('goals')

    # def post(self, request, *args, **kwargs):
    #     goal = self.get_object()
    #     today = date.today()
    #     Поправена част
    #     daily_checks = HabitCheck.objects.filter(habit=goal, date=today).count()
    #     period_checks = goal.get_current_period_checks(today=today)
    #
    #     if goal.period_unit == 'week' and daily_checks >= 1:
    #         messages.warning(
    #             request,
    #             "You've already checked in today – weekly goals allow only one check per day."
    #         )
    #     До тук
    #     elif period_checks >= goal.target_per_period:
    #         messages.warning(
    #             request,
    #             f"You've already completed your target ({goal.target_per_period}) for this {goal.period_unit}."
    #         )
    #     else:
    #         HabitCheck.objects.create(habit=goal, date=today)
    #         remaining = goal.target_per_period - (period_checks + 1)
    #         msg = (
    #             f"Check-in successful! {remaining} remaining for this {goal.period_unit}."
    #             if remaining > 0
    #             else "You've completed your goal for this period!"
    #         )
    #         messages.success(request, msg)
    #
    #     return redirect('goals')

