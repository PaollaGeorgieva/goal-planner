from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.serializers.goal_serializers import StepSerializer
from goals.models import TargetGoal
from steps.models import Step




class StepListCreateView(generics.ListCreateAPIView):
    serializer_class = StepSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Step.objects.filter(
            target_goal_id=self.kwargs['pk'],
            target_goal__user=self.request.user
        ).order_by('id')

    def perform_create(self, serializer):
        goal = get_object_or_404(
            TargetGoal,
            pk=self.kwargs['pk'],
            user=self.request.user
        )


        if goal.is_completed:
            raise ValidationError({
                "detail": "You cannot add steps on a completed goal"
            })


        serializer.save(target_goal=goal, completed=False)

class StepRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StepSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'step_pk'

    def get_queryset(self):
        return Step.objects.filter(target_goal_id=self.kwargs['pk'], target_goal__user=self.request.user)

    def update(self, request, *args, **kwargs):
        goal = TargetGoal.objects.get(pk=self.kwargs['pk'])
        if goal.is_completed:
            raise ValidationError({"detail": "You cannot edit step on completed goal"})
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        goal = TargetGoal.objects.get(pk=self.kwargs['pk'])
        if goal.is_completed:
            raise ValidationError({"detail": "You cannot edit step on completed goal"})
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        goal = TargetGoal.objects.get(pk=self.kwargs['pk'])
        if goal.is_completed:
            raise ValidationError({"detail": "You cannot delete step on completed goal"})
        return super().destroy(request, *args, **kwargs)
