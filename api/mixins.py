from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


from goals.models import TargetGoal, HabitGoal




class NoteGoalContextMixin:
    goal_kwarg = 'pk'

    def get_goal_model(self):
        goal_type = self.kwargs.get('goal_type')
        if goal_type == 'target':
            return TargetGoal
        elif goal_type == 'habit':
            return HabitGoal
        else:
            raise ValidationError({"detail": f"Unknown type of goal: {goal_type}"})

    def get_goal(self):
        model = self.get_goal_model()
        return get_object_or_404(
            model,
            pk=self.kwargs[self.goal_kwarg],
            user=self.request.user
        )

