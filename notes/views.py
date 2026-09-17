from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DeleteView

from goals.models import TargetGoal, HabitGoal
from notes.forms import NoteCreateForm, NoteEditForm
from notes.mixins import NotesGoalContextMixin
from notes.models import Note


class GoalNotesView(LoginRequiredMixin, NotesGoalContextMixin, View):
    def get(self, request, *args, **kwargs):

        notes = Note.objects.filter(
            content_type=self.content_type,
            object_id=self.goal.pk
        ).order_by("created_at")

        context = {
            "notes": notes,
            "goal": self.goal,
            "goal_type": self.goal_type,
        }

        return render(request, "notes/notes.html", context)


class CreateNoteView(LoginRequiredMixin, NotesGoalContextMixin, View):

    def get(self, request, *args, **kwargs):
        form = NoteCreateForm()
        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
        }
        return render(request, 'notes/add-note.html', context)

    def post(self, request, *args, **kwargs):

        if self.goal.is_completed:
            messages.error(request, "You cannot add note to a completed goal")
            return redirect('notes:goal-notes', goal_type=self.goal_type, pk=self.goal.pk)

        form = NoteCreateForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.content_type = self.content_type
            note.object_id = self.goal.pk
            note.save()

            return redirect('notes:goal-notes', goal_type=self.goal_type, pk=self.goal.pk)

        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
        }
        return render(request, 'notes/add-note.html', context)


class EditNoteView(LoginRequiredMixin, NotesGoalContextMixin, View):

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get('note_id')
        note = get_object_or_404(
            Note,
            pk=note_id,
            content_type=self.content_type,
            object_id=self.goal.pk
        )
        form = NoteEditForm(instance=note)
        context = {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
            'note': note,
        }
        return render(request, 'notes/add-note.html', context)

    def post(self, request, *args, **kwargs):

        if self.goal.is_completed:
            messages.error(request, "You cannot edit note on a completed goal.")
            return redirect('notes:goal-notes',goal_type=self.goal_type,pk=self.goal.pk)

        note_id = kwargs.get('note_id')
        note = get_object_or_404(
            Note,
            pk=note_id,
            content_type=self.content_type,
            object_id=self.goal.pk,
        )
        form = NoteEditForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:goal-notes', goal_type=self.goal_type, pk=self.goal.pk)

        return render(request, 'notes/add-note.html', {
            'form': form,
            'goal': self.goal,
            'goal_type': self.goal_type,
            'note': note,
        })


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note

    def get_goal(self):
        goal_type = self.kwargs['goal_type']
        goal_id = self.kwargs['pk']
        user = self.request.user

        if goal_type == 'target':
            goal_model = TargetGoal
        elif goal_type == 'habit':
            goal_model = HabitGoal
        else:
            raise Http404("Invalid goal type.")

        return get_object_or_404(
            goal_model,
            pk=goal_id,
            user=user,
        )

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
        note = self.get_object()
        goal = self.get_goal()

        if goal.is_completed:
            messages.error(request, "You cannot delete a note from a completed goal.")
            return redirect('notes:goal-notes', goal_type=kwargs['goal_type'], pk=kwargs['pk'])

        note.delete()
        return redirect('notes:goal-notes', goal_type=kwargs['goal_type'], pk=kwargs['pk'])
