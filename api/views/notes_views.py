from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.mixins import NoteGoalContextMixin
from api.serializers.goal_serializers import NoteSerializer
from notes.models import Note


class NoteListCreateView(NoteGoalContextMixin, generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        goal = self.get_goal()
        ct = ContentType.objects.get_for_model(goal)
        return Note.objects.filter(
            content_type=ct,
            object_id=goal.pk
        )

    def perform_create(self, serializer):

        goal = self.get_goal()

        serializer.save(
            content_type=ContentType.objects.get_for_model(goal),
            object_id=self.kwargs['pk'],

        )

class NoteRUDView(NoteGoalContextMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'note_pk'

    def get_queryset(self):
        goal = self.get_goal()
        ct = ContentType.objects.get_for_model(goal)
        return Note.objects.filter(
            content_type=ct,
            object_id=goal.pk
        )

    def update(self, request, *args, **kwargs):
        goal = self.get_goal()
        if goal.is_completed:
            raise ValidationError({"detail": "You cant update a note for an updated goal"})
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        goal = self.get_goal()
        if goal.is_completed:
            raise ValidationError({"detail": "You cannot delete a note on a completed goal"})
        return super().destroy(request, *args, **kwargs)