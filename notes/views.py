from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.views import View
from django.urls import reverse, reverse_lazy

from notes.forms import NoteCreateForm, NoteEditForm
from notes.mixins import NotesGoalContextMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DeleteView

from notes.models import Note
from goals.models import TargetGoal, HabitGoal


class GoalNotesView(LoginRequiredMixin, NotesGoalContextMixin, View):
    def get(self, request, *args, **kwargs):
        storage = messages.get_messages(request)
        list(storage)

        notes_queryset = Note.objects.filter(
            content_type=self.content_type,
            object_id=self.goal.pk
        ).order_by("created_at")

        context = {
            "notes": notes_queryset,
            "goal": self.goal,
            "goal_type": self.goal_type,
        }

        return render(request, "notes/notes.html", context)


class CreateNoteView(LoginRequiredMixin, NotesGoalContextMixin, View):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self.goal.is_completed:
            messages.error(request, "You cannot add note to a completed goal")
            return redirect('notes:goal-notes', goal_type=self.goal_type, pk=self.goal.pk)
        return response

    def get(self, request, *args, **kwargs):
        form = NoteCreateForm()
        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
        }
        return render(request, 'notes/add-note.html', context)

    def post(self, request, *args, **kwargs):

        form = NoteCreateForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.content_type = self.content_type
            note.object_id = self.goal.pk
            note.save()

            success_url = reverse('notes:goal-notes', kwargs={
                'goal_type': self.goal_type,
                'pk': self.goal.pk
            })
            return redirect(success_url)

        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
        }
        return render(request, 'notes/add-note.html', context)


class EditNoteView(LoginRequiredMixin, NotesGoalContextMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if self.goal.is_completed:
            messages.error(request, "You cannot edit note on a completed goal.")
            return redirect(reverse('notes:goal-notes', kwargs={
                'goal_type': kwargs.get('goal_type'),
                'pk': self.goal.pk,
            }))
        return response

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get('note_id')
        note = get_object_or_404(
            Note,
            pk=note_id,
            content_type=ContentType.objects.get_for_model(self.goal_model),
            object_id=self.goal.pk
        )
        form = NoteEditForm(instance=note)
        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': kwargs.get('goal_type'),
            'note': note,
        }
        return render(request, 'notes/add-note.html', context)

    def post(self, request, *args, **kwargs):
        note_id = kwargs.get('note_id')
        note = get_object_or_404(
            Note,
            pk=note_id,
            content_type=ContentType.objects.get_for_model(self.goal_model),
            object_id=self.goal.pk
        )
        form = NoteEditForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect(reverse('notes:goal-notes', kwargs={
                'goal_type': kwargs.get('goal_type'),
                'pk': self.goal.pk,
            }))
        return render(request, 'notes/add-note.html', {
            'form': form,
            'goal': self.goal,
            'goal_type': kwargs.get('goal_type'),
            'note': note,
        })


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note

    def get_goal(self):
        goal_id = self.kwargs['pk']
        user = self.request.user

        goal = TargetGoal.objects.filter(pk=goal_id, user=user).first()
        if not goal:
            goal = get_object_or_404(HabitGoal, pk=goal_id, user=user)
        return goal

    def get_object(self, queryset=None):
        goal = self.get_goal()
        content_type = ContentType.objects.get_for_model(goal)

        return get_object_or_404(
            Note,
            pk=self.kwargs['note_id'],
            content_type=content_type,
            object_id=goal.pk
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(reverse_lazy('notes:goal-notes', kwargs={
            'goal_type': kwargs['goal_type'],
            'pk': kwargs['pk'],
        }))
