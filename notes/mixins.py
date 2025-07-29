from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from goals.models import TargetGoal, HabitGoal

class NotesGoalContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.goal_type = kwargs.get("goal_type")
        self.goal_id = kwargs.get("pk")

        if self.goal_type == "target":
            self.goal_model = TargetGoal
        elif self.goal_type == "habit":
            self.goal_model = HabitGoal
        else:
            raise ValueError("Invalid goal type!")

        self.goal = get_object_or_404(self.goal_model, pk=self.goal_id, user=request.user)
        self.content_type = ContentType.objects.get_for_model(self.goal_model)



        return super().dispatch(request, *args, **kwargs)


