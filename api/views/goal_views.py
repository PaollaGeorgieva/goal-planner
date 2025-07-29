


from rest_framework import generics, status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


from api.serializers.goal_serializers import TargetGoalSerializer, HabitGoalSerializer, StepSerializer, NoteSerializer
from goals.models import TargetGoal, HabitGoal



class AllGoalsAPIView(APIView):
    def get(self, request):
        targets = TargetGoal.objects.filter(user=request.user).only(
            'id', 'title', 'is_completed', 'start_date', 'end_date'
        )

        habits = HabitGoal.objects.filter(user=request.user).only(
            'id', 'title', 'is_completed', 'start_date', 'period_unit'
        )

        target_data = TargetGoalSerializer(targets, many=True).data
        habit_data = HabitGoalSerializer(habits, many=True).data

        return Response({
            'target_goals': target_data,
            'habit_goals': habit_data
        })


class BaseGoalRUDView(generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_completed:
            raise ValidationError({
                "detail": "Completed goals cannot be updated"
            })
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_completed:
            raise ValidationError({
                "detail": "Completed goals cannot be partial updated"
            })
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_completed:
            raise ValidationError({
                "detail": "Completed goals cannot be deleted"
            })
        return super().destroy(request, *args, **kwargs)


class TargetGoalViewSet(BaseGoalRUDView):
    serializer_class = TargetGoalSerializer
    queryset = TargetGoal.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class HabitGoalViewSet(BaseGoalRUDView):
    serializer_class = HabitGoalSerializer
    queryset = HabitGoal.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


from rest_framework import generics


class TargetGoalCreateSet(generics.CreateAPIView):
    serializer_class = TargetGoalSerializer
    queryset = TargetGoal.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_completed=False)


class HabitGoalCreateSet(generics.CreateAPIView):
    serializer_class = HabitGoalSerializer
    queryset = HabitGoal.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_completed=False)





