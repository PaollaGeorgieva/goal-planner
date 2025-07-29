# steps/mixins.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from goals.models import TargetGoal


class GoalContextMixin:

    goal_model = None
    def dispatch(self, request, *args, **kwargs):
        self.goal_id = kwargs.get('goal_id') or kwargs.get('pk')
        self.goal = get_object_or_404(TargetGoal, pk=self.goal_id, user=request.user)
        return super().dispatch(request, *args, **kwargs)
